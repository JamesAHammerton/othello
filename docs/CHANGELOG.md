# CHANGELOG

## 2026-03-24 GMT — Add tooltip to Finish button

- `SidePanel`: added tooltip to the Finish button to satisfy the Phase 2 requirement that all buttons have tooltips.

## 2026-03-24 GMT — Update ARCHITECTURE.md for Phase 2

- Added `ai/levels.py` to the AI layer overview, table, and file layout.
- Updated `ComputerWorker` description to reference `choose_move` (was `best_move`).
- Updated AI layer module descriptions to reflect scorer hierarchy and alpha-beta.

## 2026-03-24 GMT — Fix NAIVE scorer bug; expose best_move_alpha_beta

- **Bug fix:** `best_move` and `_minimax` now accept a `scorer` parameter (default `score_amateur`). Previously `_minimax` hardcoded `score_amateur`, so the NAIVE level silently used the wrong scorer.
- `choose_move` now passes `config.scorer` to `best_move`, so each level uses its configured scorer correctly.
- Renamed `_best_move_alpha_beta` → `best_move_alpha_beta` (public API; it was already imported across modules).
- Added `TestScoreAlias` to `test_scorer.py` to guard the `score = score_amateur` alias.
- Added `test_naive_uses_score_naive` and `test_amateur_uses_score_amateur` to `test_levels.py`.

---

## 2026-03-21 GMT — Phase 2: five AI levels with alpha-beta pruning

### Changes

**Game layer (`game/`)**
- Added `C_SQUARES` constant to `game/rules.py`: 8 edge squares adjacent to the four corners

**AI layer (`ai/`)**
- Renamed `scorer.score` → `score_amateur`; added `score_naive` (piece count only), `score_experienced` (amateur + C-square penalty), `score_expert` (experienced + mobility). Added `Scorer` type alias. `score` alias retained for backward compatibility.
- Added `_alpha_beta` and `_best_move_alpha_beta` to `ai/minimax.py`; accepts a `Scorer` callable. Existing `best_move`/`_minimax` unchanged.
- Added new module `ai/levels.py`: `PlayerLevel` enum (DUMB/NAIVE/AMATEUR/EXPERIENCED/EXPERT), `LevelConfig` dataclass, `LEVEL_CONFIGS`, `LEVEL_ORDER`, `DEFAULT_LEVEL`, `choose_move()`, `next_level()`.

**UI layer (`ui/`)**
- `ComputerWorker`: accepts `PlayerLevel`; calls `choose_move()` instead of `best_move()`.
- `LaunchWindow`: added level-cycle button (displays current level name, tooltip shows strategy description); added tooltips to Play and Quit buttons.
- `SidePanel`: added level name/description labels and White/Black player identity labels; new `set_level()` and `set_players()` methods.
- `GameWindow`: accepts `PlayerLevel`; calls `side_panel.set_level()` and `side_panel.set_players()` on init; passes level to `ComputerWorker`.

**Tests**
- Added `TestCSquares` to `tests/game/test_rules.py`
- Replaced `TestScore` with `TestScoreNaive`, `TestScoreAmateur`, `TestScoreExperienced`, `TestScoreExpert` in `tests/ai/test_scorer.py`
- Added `TestBestMoveAlphaBeta` to `tests/ai/test_minimax.py`
- Added new `tests/ai/test_levels.py`: `TestLevelOrder`, `TestDefaultLevel`, `TestNextLevel`, `TestChooseMove`

---

## 2026-03-21 GMT — MVP implementation

### Changes

**Game layer (`game/`)**
- Implemented `Board`: dict-backed 8×8 state; `__init__` sets standard starting position; `empty`, `get`, `place`, `remove`, `copy`, `piece_counts`, `all_pieces`, `__eq__`, `__repr__`
- Implemented `rules`: `opponent`, `flipped_squares` (ray-casting), `legal_moves`, `apply_move` (returns new `Board`; raises `ValueError` if illegal), `is_game_over`
- Implemented `Game`: mutable wrapper; `__init__` sets black as first player; `apply_move`, `pass_turn` mutate state; properties for `board`, `current_player`, `human_colour`, `computer_colour`, `turn_count`

**AI layer (`ai/`)**
- Implemented `scorer.score`: `piece_diff + 10*corner_diff + 10*diagonal_corner_penalty` per requirements
- Implemented `minimax.best_move` and `_minimax`: minimax to configurable depth (default 4), pass-aware, random tie-breaking

**UI layer (`ui/`)**
- Implemented `SidePanel`: score label (`W / B`), turns label, hidden Finish button revealed on game end
- Implemented `ComputerWorker`: `QRunnable` that calls `best_move` on a thread-pool thread and emits `signals.move_ready`
- Implemented `BoardWidget`: paints 8×8 grid with axis labels, ~1 cm squares (physical-DPI-aware), legal-move shading, per-square highlights (bright green / red), white/black piece circles; emits `square_clicked`
- Implemented `LaunchWindow`: three-button layout; creates `GameWindow` with `self` as launch reference, then hides
- Implemented `GameWindow`: full turn loop — game-over check, pass detection (modal popup), human click handling (legal/illegal highlights via `QTimer`), computer moves via `ComputerWorker` + `QTimer` delay; `_on_finish` closes and restores `LaunchWindow`

**Tests**
- Implemented all 41 stub tests across `tests/game/` and `tests/ai/`; all pass

**Housekeeping**
- Removed `[tool.ruff.lint.per-file-ignores]` F401 suppression (no longer needed)
- Updated `README.md` with usage and architecture overview
- Updated `CODE_STRUCTURE.md`: `GameWindow.__init__` now takes `(human_colour, launch_window)`

---

## 2026-03-19 23:57 GMT — Ruff linting configuration

### Changes
- Added `[tool.ruff.lint]` config to `pyproject.toml` enabling rule sets: E, F, I, N, UP, B, RUF, PT
- Added `per-file-ignores` suppressing `F401` in `tests/` and `ui/` (unused imports expected in stubs)
- Fixed `I001`: sorted imports in test files and `ui/board_widget.py`
- Fixed `RUF002`: replaced ambiguous `×` character with `x` in docstrings in `game/board.py` and `ui/board_widget.py`

### Reasoning
Enabling a broad but practical ruleset early catches issues as code is written rather than in bulk later. Suppressing `F401` for stub files avoids noise until implementations are in place, at which point the ignores will be removed.

---

## 2026-03-19 23:44 GMT — Formatting and conventions

### Changes
- Removed redundant `from __future__ import annotations` from all source files (Python ≥ 3.13 supports all type hint syntax natively)
- Applied `ruff format` to bring all files into compliance with the project's formatting standard
- Added explanatory comment to `DIRECTIONS` in `game/rules.py`
- Updated `CLAUDE.md` to mandate `ruff format` after changes and to specify GMT timestamps in CHANGELOG entries

### Reasoning
Establishing consistent formatting early avoids noisy diffs later. Documenting the conventions in `CLAUDE.md` ensures they are applied automatically in future sessions.

---

## 2026-03-19 23:34 GMT — Initial project scaffold

### Changes
- Added `docs/REQUIREMENTS.md` defining the MVP feature set
- Added `docs/ARCHITECTURE.md` describing the three-layer design (game, AI, UI)
- Added `docs/CODE_STRUCTURE.md` as a living index of all modules and public symbols
- Created stub modules with typed signatures and docstrings but no implementation:
  - `game/board.py` — `Board` class and `Colour`/`Square` type aliases
  - `game/rules.py` — stateless rule functions (`legal_moves`, `apply_move`, etc.)
  - `game/game.py` — mutable `Game` state container
  - `ai/scorer.py` — board evaluation function
  - `ai/minimax.py` — minimax search with random tie-breaking
  - `ui/launch_window.py` — initial window with Play/Quit buttons
  - `ui/game_window.py` — game window orchestrating the turn loop
  - `ui/board_widget.py` — painted board widget with click handling
  - `ui/side_panel.py` — score, turn count, and Finish button
  - `ui/computer_worker.py` — `QRunnable` for off-thread minimax computation
- Created stub test files covering all game, rules, game-state, scorer, and minimax behaviours
- Updated `main.py` to create `QApplication` and show `LaunchWindow`

### Reasoning
Establishing the full module structure and signatures before any implementation makes the intended boundaries explicit and avoids having to reorganise code mid-development. Stub tests written alongside the stubs ensure that the test surface is planned in advance and that TDD can proceed module by module without gaps. The three-layer split (game logic, AI, Qt UI) keeps the first two layers free of Qt dependencies, making them fast and straightforward to unit-test.
