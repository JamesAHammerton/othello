# CHANGELOG

## 2026-03-19 — Initial project scaffold

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
