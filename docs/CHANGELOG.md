# CHANGELOG

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
