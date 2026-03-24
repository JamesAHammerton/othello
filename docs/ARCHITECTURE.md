# ARCHITECTURE

## Overview

The application follows a layered architecture with a clear separation between game logic (model), AI, and UI (view). Qt signals/slots are used to communicate between layers without coupling them.

```
┌─────────────────────────────────────────┐
│                   UI Layer              │
│  LaunchWindow  GameWindow  BoardWidget  │
│            SidePanel  ComputerWorker    │
├─────────────────────────────────────────┤
│                  Game Layer             │
│          Game  Board  Rules             │
├─────────────────────────────────────────┤
│                   AI Layer              │
│       Levels  Minimax  Scorer           │
└─────────────────────────────────────────┘
```

---

## Layers

### Game Layer (`game/`)

Pure Python — no Qt dependency. Fully unit-testable in isolation.

| Module | Responsibility |
|--------|---------------|
| `game/board.py` | Immutable-friendly `Board` class: 8×8 state, piece placement, flip calculation |
| `game/rules.py` | Stateless functions: `legal_moves(board, colour)`, `apply_move(board, colour, square)`, `is_game_over(board)` |
| `game/game.py` | `Game` class: mutable game state (board, current player, turn count); exposes methods consumed by the UI |

**Key types:**

```
Colour: Literal["white", "black"]
Square: tuple[int, int]   # (col 0-7, row 0-7)  e.g. A1 = (0,0)
Board:  8×8 grid of Colour | None
```

---

### AI Layer (`ai/`)

Pure Python — no Qt dependency. Fully unit-testable in isolation.

| Module | Responsibility |
|--------|---------------|
| `ai/scorer.py` | Heuristic functions (`score_naive`, `score_amateur`, `score_experienced`, `score_expert`) returning `int` score differentials |
| `ai/minimax.py` | `best_move` (minimax) and `best_move_alpha_beta` — tree search with random tie-breaking |
| `ai/levels.py` | `PlayerLevel` enum, per-level `LevelConfig`, and `choose_move` — the single public AI entry point |

The search functions call `rules.legal_moves` and `rules.apply_move` to explore the tree. `choose_move` selects the appropriate algorithm and scorer for the requested `PlayerLevel`.

---

### UI Layer (`ui/`)

PySide6 (Qt6). No game logic lives here — the UI reads from and writes to `Game` objects.

| Module | Responsibility |
|--------|---------------|
| `ui/launch_window.py` | `LaunchWindow(QMainWindow)` — Play as White / Play as Black / Quit buttons |
| `ui/game_window.py` | `GameWindow(QMainWindow)` — hosts `SidePanel` (left) and `BoardWidget` (right); orchestrates turn flow |
| `ui/board_widget.py` | `BoardWidget(QWidget)` — paints the board; emits `square_clicked(Square)` signal; handles highlight states |
| `ui/side_panel.py` | `SidePanel(QWidget)` — displays score, turn count, and post-game Finish button |
| `ui/computer_worker.py` | `ComputerWorker(QRunnable)` — runs `ai.levels.choose_move` off the main thread; emits `move_ready(Square)` via a `WorkerSignals(QObject)` helper |

---

## Control Flow

### Starting a game

```
LaunchWindow ──"Play as White/Black"──► GameWindow(colour)
GameWindow creates Game, shows window, triggers first turn
```

### Turn loop (inside `GameWindow`)

```
_start_turn()
  ├─ Check game over → show result popup / enable Finish button
  ├─ Check no legal moves → show pass popup → _start_turn() for opponent
  ├─ Human turn → enable board clicks; wait for square_clicked signal
  └─ Computer turn → submit ComputerWorker to QThreadPool
                       └─ on move_ready → _handle_move(square)

_handle_move(square)
  ├─ Highlight square (bright green or red for illegal human click)
  ├─ QTimer.singleShot(500, _apply_move)   ← non-blocking 500 ms delay
  └─ _apply_move() → game.apply_move() → board repaint → _start_turn()
```

### Returning to launch

```
Finish button → GameWindow.close() → LaunchWindow.show()
```

---

## Threading Model

- The main (Qt) thread owns all UI and `Game` state.
- `ComputerWorker` runs on a `QThreadPool` thread. It receives an immutable copy of the board and colour — it never touches shared state.
- The worker emits `move_ready(Square)` which is delivered to the main thread via a queued connection, so no locking is required.

---

## UI Layout

```
GameWindow
├── QHBoxLayout
│   ├── SidePanel (fixed width)
│   │   ├── QLabel  "Score: W / B"
│   │   ├── QLabel  "Turns: N"
│   │   └── QPushButton "Finish"  (hidden until game over)
│   └── BoardWidget
│       └── paintEvent draws 8×8 grid + pieces + highlights
```

**Square sizing:** `BoardWidget.paintEvent` reads `QScreen.physicalDotsPerInch()` to compute a pixel size such that each square is ~1 cm × 1 cm regardless of display scaling.

---

## File Layout

```
othello/
├── main.py                  # QApplication entry point
├── game/
│   ├── __init__.py
│   ├── board.py
│   ├── rules.py
│   └── game.py
├── ai/
│   ├── __init__.py
│   ├── scorer.py
│   ├── minimax.py
│   └── levels.py
├── ui/
│   ├── __init__.py
│   ├── launch_window.py
│   ├── game_window.py
│   ├── board_widget.py
│   ├── side_panel.py
│   └── computer_worker.py
└── tests/
    ├── game/
    │   ├── test_board.py
    │   ├── test_rules.py
    │   └── test_game.py
    └── ai/
        ├── test_scorer.py
        └── test_minimax.py
```

---

## Design Constraints

- **No game logic in the UI layer.** `BoardWidget` and `GameWindow` call into `game/` and `ai/`; they do not implement rules themselves.
- **No Qt in the game or AI layers.** This keeps those layers fast to test and free of Qt lifecycle issues.
- **All 500 ms delays via `QTimer.singleShot`.** Never `time.sleep` on the main thread.
- **All blocking computation (minimax) off the main thread.** Always via `QThreadPool` + `QRunnable`.
- **Popups block game actions, not the event loop.** Use non-modal dialogs or `QMessageBox.exec()` only after disabling board interaction; re-enable on `accepted`.