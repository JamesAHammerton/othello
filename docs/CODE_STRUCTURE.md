# CODE STRUCTURE

Current state of the codebase. Update this file whenever modules, classes, or public functions are added, removed, or renamed.

---

## `main.py`

Entry point. Creates `QApplication`, instantiates `LaunchWindow`, and starts the Qt event loop.

---

## `game/`

Pure Python — no Qt dependency.

### `game/board.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `Colour` | type alias | `Literal["white", "black"]` |
| `Square` | type alias | `tuple[int, int]` — `(col, row)`, 0-indexed; A1 = `(0,0)` |
| `INITIAL_SQUARES` | constant | Starting piece positions |
| `Board` | class | 8×8 board state |
| `Board.__init__` | method | Constructs board in standard starting position |
| `Board.empty` | classmethod | Returns a completely empty board |
| `Board.get` | method | Returns the colour at a square, or `None` |
| `Board.place` | method | Places a piece in-place |
| `Board.remove` | method | Removes a piece in-place |
| `Board.copy` | method | Returns a deep copy |
| `Board.piece_counts` | method | Returns `(white_count, black_count)` |
| `Board.all_pieces` | method | Returns list of `(square, colour)` for all occupied squares |

### `game/rules.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `DIRECTIONS` | constant | 8 directional vectors for ray-casting |
| `CORNERS` | constant | The four corner squares |
| `legal_moves` | function | `(board, colour) -> list[Square]` |
| `flipped_squares` | function | `(board, colour, square) -> list[Square]` — empty if illegal |
| `apply_move` | function | `(board, colour, square) -> Board` — returns new board; raises `ValueError` if illegal |
| `is_game_over` | function | `(board) -> bool` — True when neither player can move |
| `opponent` | function | `(colour) -> Colour` — returns the opposite colour |

### `game/game.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `Game` | class | Mutable game-state container |
| `Game.__init__` | method | `(human_colour)` — creates board, sets first player to black |
| `Game.board` | property | Current `Board` |
| `Game.current_player` | property | `Colour` whose turn it is |
| `Game.human_colour` | property | Human's `Colour` |
| `Game.computer_colour` | property | Computer's `Colour` |
| `Game.turn_count` | property | Number of turns played so far |
| `Game.score` | method | `() -> (white_count, black_count)` |
| `Game.legal_moves` | method | `() -> list[Square]` for current player |
| `Game.is_over` | method | `() -> bool` |
| `Game.is_human_turn` | method | `() -> bool` |
| `Game.apply_move` | method | `(square)` — mutates state; raises `ValueError` if illegal |
| `Game.pass_turn` | method | `()` — passes and advances player |

---

## `ai/`

Pure Python — no Qt dependency.

### `ai/scorer.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `score` | function | `(board, colour) -> int` — minimax evaluation function |

### `ai/minimax.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `best_move` | function | `(board, colour, depth=4) -> Square` — public entry point |
| `_minimax` | function | `(board, colour, maximising_colour, depth) -> int` — recursive helper |

---

## `ui/`

PySide6 (Qt6). No game logic.

### `ui/launch_window.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `LaunchWindow` | class | `QMainWindow` — initial window with Play/Quit buttons |
| `LaunchWindow.__init__` | method | Builds and shows the window |
| `LaunchWindow._on_play_white` | method | Opens `GameWindow` with human as White |
| `LaunchWindow._on_play_black` | method | Opens `GameWindow` with human as Black |
| `LaunchWindow._on_quit` | method | Quits the application |

### `ui/game_window.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `GameWindow` | class | `QMainWindow` — hosts `SidePanel` + `BoardWidget`, drives turn loop |
| `GameWindow.__init__` | method | `(human_colour)` — creates `Game`, lays out widgets, starts first turn |
| `GameWindow._start_turn` | method | Checks game-over / pass / dispatches human or computer turn |
| `GameWindow._handle_square_clicked` | method | Handles human board click; highlights green or red |
| `GameWindow._handle_move` | method | Highlights chosen square, schedules `_apply_move` via `QTimer` |
| `GameWindow._apply_move` | method | Commits move to `Game`, repaints, calls `_start_turn` |
| `GameWindow._handle_computer_move` | method | Slot for `ComputerWorker.signals.move_ready` |
| `GameWindow._show_pass_popup` | method | Modal dialog for a forced pass |
| `GameWindow._show_game_over_popup` | method | Modal dialog announcing game end |
| `GameWindow._on_finish` | method | Closes window, shows `LaunchWindow` |

### `ui/board_widget.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `HIGHLIGHT_NONE` | constant | `"none"` |
| `HIGHLIGHT_LEGAL` | constant | `"legal"` — bright green |
| `HIGHLIGHT_ILLEGAL` | constant | `"illegal"` — red |
| `BoardWidget` | class | `QWidget` — paints board and emits clicks |
| `BoardWidget.square_clicked` | signal | `Signal(tuple)` — emits `Square` |
| `BoardWidget.__init__` | method | Initialises state and sizing |
| `BoardWidget.set_board` | method | `(board)` — updates displayed state |
| `BoardWidget.set_legal_moves` | method | `(squares)` — marks squares light green |
| `BoardWidget.set_highlight` | method | `(square, highlight)` — highlights one square |
| `BoardWidget.clear_highlight` | method | Removes single-square highlight |
| `BoardWidget.set_interactive` | method | `(enabled)` — enables/disables click handling |
| `BoardWidget.paintEvent` | method | Qt override — draws grid, labels, pieces, highlights |
| `BoardWidget.mousePressEvent` | method | Qt override — translates click to `square_clicked` |
| `BoardWidget._square_size_px` | method | Returns pixel size of one square (~1 cm at physical DPI) |
| `BoardWidget._square_at` | method | `(x, y) -> Square | None` |

### `ui/side_panel.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `SidePanel` | class | `QWidget` — score, turn count, Finish button |
| `SidePanel.finish_clicked` | signal | `Signal()` |
| `SidePanel.__init__` | method | Builds labels and hidden Finish button |
| `SidePanel.update_score` | method | `(white, black)` — updates score label |
| `SidePanel.update_turns` | method | `(count)` — updates turn label |
| `SidePanel.show_finish_button` | method | Makes Finish button visible |
| `SidePanel._on_finish_clicked` | method | Emits `finish_clicked` |

### `ui/computer_worker.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `WorkerSignals` | class | `QObject` — holds signals for `ComputerWorker` |
| `WorkerSignals.move_ready` | signal | `Signal(tuple)` — emits `Square` |
| `ComputerWorker` | class | `QRunnable` — runs minimax off the main thread |
| `ComputerWorker.__init__` | method | `(board, colour)` — stores immutable board copy |
| `ComputerWorker.run` | method | Calls `best_move`, emits `signals.move_ready` |

---

## `tests/`

### `tests/game/test_board.py`
`TestBoardInit`, `TestBoardGet`, `TestBoardPlace`, `TestBoardRemove`, `TestBoardCopy`, `TestBoardPieceCounts`

### `tests/game/test_rules.py`
`TestOpponent`, `TestLegalMoves`, `TestFlippedSquares`, `TestApplyMove`, `TestIsGameOver`

### `tests/game/test_game.py`
`TestGameInit`, `TestGameScore`, `TestGameApplyMove`, `TestGamePassTurn`, `TestGameIsOver`

### `tests/ai/test_scorer.py`
`TestScore`

### `tests/ai/test_minimax.py`
`TestBestMove`
