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

# Type check
uv run mypy . --exclude .venv
```

## How to play

1. Launch the application. The launch window appears.
2. Choose a difficulty level using the **Level** button (cycles through Dumb → Naive → Amateur → Experienced → Expert). Hover for a description of each level's strategy.
3. Click **Play as White** or **Play as Black** to start. Black always moves first.
4. Click a highlighted (light green) square to place your piece.
   - If you click an illegal square it flashes red for 0.5 s; try again.
5. The computer thinks and plays automatically.
6. When a player has no legal move, a pass dialog appears. Click **OK** to continue.
7. When the game ends, click **Finish** to return to the launch window.

## AI difficulty levels

| Level | Algorithm | Depth | Heuristic |
|---|---|---|---|
| Dumb | Random | — | None |
| Naive | Minimax | 2 | Piece count |
| Amateur | Minimax | 4 | Piece count + corners + X-squares |
| Experienced | Alpha-beta | 6 | Amateur + C-squares |
| Expert | Alpha-beta | 6 | Experienced + mobility |

## Architecture

Three-layer design — game logic, AI, and UI are fully decoupled:

```
UI layer    (ui/)     — PySide6 widgets, no game logic
AI layer    (ai/)     — search, scoring, and level selection, pure Python
Game layer  (game/)   — Board, rules, and Game state, pure Python
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for full details.
