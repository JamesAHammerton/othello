# TODO

Tracks planned features, enhancements, and refactors not yet implemented.

## Format

Each entry has the form:

```
## TODO-N — YYYY-MM-DD HH:MM GMT — Title
**Status:** OPEN | IMPLEMENTED | DROPPED

Description of the work to be done.
```

Entries are ordered oldest-first. Update the status in-place when an item is completed or
abandoned.

---

## TODO-1 — 2026-03-24 03:27 GMT — Define stable disc detection in `game/rules.py`
**Status:** OPEN

Add a `stable_discs(board: Board, colour: Colour) -> list[Square]` function that returns all
squares occupied by `colour` that can never be flipped for the remainder of the game.

A disc is stable if it satisfies all four directional axes (horizontal, vertical, and both
diagonals): on each axis, either the disc is on an edge/corner, or both directions along
that axis are fully occupied (so there is no gap through which an opponent disc could be
placed to flank it). Corners are unconditionally stable; their neighbours become stable once
an adjacent corner and edge-fill conditions are met.

Write unit tests in `tests/game/test_rules.py` covering: an empty board (no stable discs),
a board where only a corner is occupied (one stable disc), and a board with a fully-filled
edge (all edge discs stable).

---

## TODO-2 — 2026-03-24 03:28 GMT — Add `score_master` and `score_endgame` to `ai/scorer.py`
**Status:** OPEN

Add two new scoring functions:

**`score_endgame(board: Board, colour: Colour) -> int`** — returns the exact final piece
count differential (`own_pieces - opp_pieces`). Used in the last few moves when the outcome
can be determined precisely. Kept separate from `score_naive` to make intent clear.

**`score_master(board: Board, colour: Colour) -> int`** — extends `score_expert` with a
stability term:

```
score_expert + 20 * (own_stable - opp_stable)
```

The weight of 20 reflects that stable discs are permanently secured and worth significantly
more than a mobility advantage. Import `stable_discs` from `game/rules`.

Write tests in `tests/ai/test_scorer.py` covering: symmetry for both functions (swapping
colours negates the score), stability term is zero when neither player holds stable discs,
stability term is positive when the scoring player holds a corner, and `score_endgame`
equals piece count differential.

---

## TODO-3 — 2026-03-24 03:29 GMT — Add endgame switching to `ai/minimax.py`
**Status:** OPEN

Add a `best_move_endgame(board, colour, depth, scorer, endgame_threshold, endgame_scorer) -> Square`
function that delegates to `best_move_alpha_beta` normally, but switches to
`endgame_scorer` (exact piece count) when the number of empty squares is at or below
`endgame_threshold`. A threshold of 12 empty squares is a reasonable default.

The switch happens inside the recursive search: pass a wrapper scorer to `_alpha_beta` that
calls `endgame_scorer` instead of `scorer` once empty squares fall to or below the
threshold.

Write tests in `tests/ai/test_minimax.py` verifying: that `best_move_endgame` returns a
legal move on a standard board, and that it returns the same move as plain alpha-beta on a
mid-game board where the endgame threshold has not been reached.

---

## TODO-4 — 2026-03-24 03:30 GMT — Add `MASTER` level to `ai/levels.py`
**Status:** OPEN

Add `PlayerLevel.MASTER = "master"` to the `PlayerLevel` enum and a corresponding entry in
`LEVEL_CONFIGS`:

- `name`: `"Master"`
- `description`: `"Looks 8 moves ahead; weights stable discs and corners; plays perfectly in the endgame. Uses alpha-beta pruning."`
- `depth`: `8`
- `scorer`: `score_master`
- `use_alpha_beta`: `True`
- endgame threshold: 12 empty squares (uses `best_move_endgame` in `choose_move`)

`LevelConfig` will need an optional `endgame_threshold: int | None = None` field. `choose_move`
checks this field and calls `best_move_endgame` instead of `best_move_alpha_beta` when set.

Append `MASTER` to `LEVEL_ORDER` after `EXPERT`. Update tests in `tests/ai/test_levels.py`:
`LEVEL_ORDER` now has 6 entries, `next_level` wraps from `MASTER` back to `DUMB`, and
`choose_move` with `MASTER` returns a legal move.

---

## TODO-5 — 2026-03-24 03:30 GMT — Wire `MASTER` level through the UI
**Status:** OPEN

Update `ui/launch_window.py`, `ui/side_panel.py`, and `ui/game_window.py` to support the
new level — no structural changes required since the UI already iterates `LEVEL_ORDER` and
reads descriptions from `LEVEL_CONFIGS`. Confirm by running the game and cycling through
levels to verify Master appears with the correct description in both the launch window
tooltip and the side panel.

---
