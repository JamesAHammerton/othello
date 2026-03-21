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
| `C_SQUARES` | constant | 8 edge squares immediately adjacent to the corners |
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
| `Scorer` | type alias | `Callable[[Board, Colour], int]` — scorer function signature |
| `DIAGONAL_CORNERS` | constant | 4 X-squares (diagonal to corners) |
| `score_naive` | function | `(board, colour) -> int` — raw piece count differential |
| `score_amateur` | function | `(board, colour) -> int` — naive + corner bonus + X-square penalty |
| `score_experienced` | function | `(board, colour) -> int` — amateur + C-square penalty |
| `score_expert` | function | `(board, colour) -> int` — experienced + mobility term |
| `score` | alias | Alias for `score_amateur` (backward compatibility) |

### `ai/minimax.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `best_move` | function | `(board, colour, depth=4) -> Square` — minimax entry point; uses `score_amateur` |
| `_minimax` | function | `(board, colour, maximising_colour, depth) -> int` — recursive minimax helper |
| `_best_move_alpha_beta` | function | `(board, colour, depth, scorer) -> Square` — alpha-beta entry point with custom scorer |
| `_alpha_beta` | function | `(board, colour, maximising_colour, depth, alpha, beta, scorer) -> int` — recursive alpha-beta helper |

### `ai/levels.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `PlayerLevel` | enum | `DUMB`, `NAIVE`, `AMATEUR`, `EXPERIENCED`, `EXPERT` |
| `LevelConfig` | dataclass | `name`, `description`, `depth`, `scorer`, `use_alpha_beta` |
| `LEVEL_CONFIGS` | constant | `dict[PlayerLevel, LevelConfig]` — config for each level |
| `LEVEL_ORDER` | constant | `[DUMB, NAIVE, AMATEUR, EXPERIENCED, EXPERT]` |
| `DEFAULT_LEVEL` | constant | `PlayerLevel.AMATEUR` |
| `next_level` | function | `(level) -> PlayerLevel` — cycles through `LEVEL_ORDER`, wrapping |
| `choose_move` | function | `(board, colour, level) -> Square` — public AI entry point |

---

## `ui/`

PySide6 (Qt6). No game logic.

### `ui/launch_window.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `LaunchWindow` | class | `QMainWindow` — initial window with level selection, Play/Quit buttons |
| `LaunchWindow.__init__` | method | Builds the window (caller must call `show()`) |
| `LaunchWindow._update_level_button` | method | Refreshes level button text and tooltip from current level config |
| `LaunchWindow._on_cycle_level` | method | Advances to next level and updates button |
| `LaunchWindow._on_play_white` | method | Opens `GameWindow` with human as White, hides self |
| `LaunchWindow._on_play_black` | method | Opens `GameWindow` with human as Black, hides self |
| `LaunchWindow._on_quit` | method | Quits the application |

### `ui/game_window.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `GameWindow` | class | `QMainWindow` — hosts `SidePanel` + `BoardWidget`, drives turn loop |
| `GameWindow.__init__` | method | `(human_colour, launch_window, level)` — creates `Game`, initialises side panel, shows window, starts first turn |
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
| `SidePanel` | class | `QWidget` — level info, player colours, score, turn count, Finish button |
| `SidePanel.finish_clicked` | signal | `Signal()` |
| `SidePanel.__init__` | method | Builds labels and hidden Finish button |
| `SidePanel.set_level` | method | `(level)` — updates level name and description labels |
| `SidePanel.set_players` | method | `(human_colour)` — sets White/Black identity labels |
| `SidePanel.update_score` | method | `(white, black)` — updates score label |
| `SidePanel.update_turns` | method | `(count)` — updates turn label |
| `SidePanel.show_finish_button` | method | Makes Finish button visible |
| `SidePanel._on_finish_clicked` | method | Emits `finish_clicked` |

### `ui/computer_worker.py`

| Symbol | Kind | Description |
|--------|------|-------------|
| `WorkerSignals` | class | `QObject` — holds signals for `ComputerWorker` |
| `WorkerSignals.move_ready` | signal | `Signal(tuple)` — emits `Square` |
| `ComputerWorker` | class | `QRunnable` — runs `choose_move` off the main thread |
| `ComputerWorker.__init__` | method | `(board, colour, level)` — stores board copy, colour, and level |
| `ComputerWorker.run` | method | Calls `choose_move`, emits `signals.move_ready` |

---

## `tests/`

### `tests/game/test_board.py`
`TestBoardInit`, `TestBoardGet`, `TestBoardPlace`, `TestBoardRemove`, `TestBoardCopy`, `TestBoardPieceCounts`

### `tests/game/test_rules.py`
`TestCSquares`, `TestOpponent`, `TestLegalMoves`, `TestFlippedSquares`, `TestApplyMove`, `TestIsGameOver`

### `tests/game/test_game.py`
`TestGameInit`, `TestGameScore`, `TestGameApplyMove`, `TestGamePassTurn`, `TestGameIsOver`

### `tests/ai/test_scorer.py`
`TestScoreNaive`, `TestScoreAmateur`, `TestScoreExperienced`, `TestScoreExpert`

### `tests/ai/test_minimax.py`
`TestBestMove`, `TestBestMoveAlphaBeta`

### `tests/ai/test_levels.py`
`TestLevelOrder`, `TestDefaultLevel`, `TestNextLevel`, `TestChooseMove`
