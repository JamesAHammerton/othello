# Othello

A human-vs-computer Othello (Reversi) game built with Python and PySide6 (Qt6).

## Requirements

- Python ≥ 3.13
- [uv](https://github.com/astral-sh/uv) (dependency manager)

## Running the game

```bash
uv run python main.py
```

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

## How to play

1. Launch the application. The launch window appears with three buttons:
   - **Play as White** — you play White, the computer plays Black.
   - **Play as Black** — you play Black, the computer plays White. Black moves first.
   - **Quit** — exits the application.
2. Click a highlighted (light green) square to place your piece.
   - If you click an illegal square it flashes red for 0.5 s; try again.
3. The computer thinks using minimax search (depth 4) and plays automatically.
4. When a player has no legal move, a pass dialog appears. Click **OK** to continue.
5. When the game ends, click **Finish** to return to the launch window.

## Architecture

Three-layer design — game logic, AI, and UI are fully decoupled:

```
UI layer    (ui/)     — PySide6 widgets, no game logic
AI layer    (ai/)     — minimax search and board scorer, pure Python
Game layer  (game/)   — Board, rules, and Game state, pure Python
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for full details.
