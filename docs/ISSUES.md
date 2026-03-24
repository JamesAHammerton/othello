# ISSUES

Tracks bugs, correctness problems, and other concerns identified during code review.

## Format

Each entry has the form:

```
## ISSUE-N — YYYY-MM-DD HH:MM GMT — Title
**Status:** OPEN | FIXED | DROPPED

Description of the issue, where it occurs, and why it matters.
```

Entries are ordered oldest-first. Update the status in-place when an issue is resolved.

---

## ISSUE-1 — 2026-03-24 14:00 GMT — ComputerWorker silently swallows exceptions
**Status:** OPEN

`ui/computer_worker.py:36-39` — If `choose_move` raises (e.g. the board position has no
legal moves due to a bug, or a scorer throws), `QRunnable` drops the exception and
`move_ready` is never emitted. The game hangs indefinitely with no error shown to the user.

Should catch exceptions in `run()`, log or report them, and either emit a fallback signal or
close the game window gracefully.

---

## ISSUE-2 — 2026-03-24 14:00 GMT — Passes consume search depth
**Status:** OPEN

`ai/minimax.py:57` and `ai/minimax.py:144` — When a player has no legal moves,
both `_minimax` and `_alpha_beta` recurse with `depth - 1`. A forced pass costs one level
of the depth budget, so in late-game positions where passes are common the AI effectively
searches fewer real plies than the configured depth. Stronger levels (depth 6 and 8) are
most affected.

The standard fix is not to decrement depth when recursing through a pass, so that depth
counts plies of actual moves rather than pass events.

---

## ISSUE-3 — 2026-03-24 14:00 GMT — Alpha-beta tie-breaking can be skewed
**Status:** OPEN

`ai/minimax.py:96-113` — `best_move_alpha_beta` updates `alpha` as it evaluates root
moves, then collects all returned scores for tie-breaking. Moves evaluated after the first
(when `alpha > -inf`) may be pruned and return an inexact (lower-than-true) score. A move
whose real minimax value equals the best score may appear worse and be excluded from the
tie-break pool, making the random tie-breaking non-uniform across truly equal moves.

This does not affect which move is chosen as best (the optimal move is still returned), but
skews the randomness among equally-valued alternatives.

---

## ISSUE-4 — 2026-03-24 14:00 GMT — assert used in production turn-loop path
**Status:** OPEN

`ui/game_window.py:125` — `assert self._pending_square is not None` guards the application
of a pending move. Python's `-O` flag silently disables all `assert` statements, so this
check would be skipped in an optimised build, leading to a `TypeError` or incorrect
behaviour rather than a clear error message.

Replace with an explicit guard (e.g. `if self._pending_square is None: return` or raise a
`RuntimeError`).

---

## ISSUE-5 — 2026-03-24 14:00 GMT — score alias comment is stale
**Status:** OPEN

`ai/scorer.py:77` — The `score = score_amateur` alias carries the comment "backward
compatibility with existing minimax code", but `minimax.py` already imports `score_amateur`
directly and does not use `score`. The alias is only referenced in `test_scorer.py`. The
comment is misleading; either remove the alias or update the comment to reflect its actual
purpose (test coverage of the alias).

---

## ISSUE-6 — 2026-03-24 14:00 GMT — docs/PHASE2_PLAN.md is untracked
**Status:** DROPPED

`docs/PHASE2_PLAN.md` was never committed to git. If this file is intended as a permanent
planning record it should be committed; if it is a temporary working document it should be
deleted or added to `.gitignore`.
