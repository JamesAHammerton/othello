import random

from ai.scorer import score
from game.board import Board, Colour, Square
from game.rules import apply_move, is_game_over, legal_moves, opponent


def best_move(board: Board, colour: Colour, depth: int = 4) -> Square:
    """Return the best move for *colour* using minimax search to *depth*.

    Ties in score are broken by random selection among the tied moves.

    Raises ValueError if there are no legal moves for *colour*.
    """
    moves = legal_moves(board, colour)
    if not moves:
        raise ValueError(f"No legal moves for {colour}")

    scored: list[tuple[int, Square]] = []
    for sq in moves:
        new_board = apply_move(board, colour, sq)
        s = _minimax(new_board, opponent(colour), colour, depth - 1)
        scored.append((s, sq))

    best_score = max(s for s, _ in scored)
    best_moves = [sq for s, sq in scored if s == best_score]
    return random.choice(best_moves)


def _minimax(
    board: Board,
    colour: Colour,
    maximising_colour: Colour,
    depth: int,
) -> int:
    """Recursive minimax helper.

    Args:
        board: Current board state.
        colour: The player whose turn it is at this node.
        maximising_colour: The root player (whose perspective we score from).
        depth: Remaining search depth.

    Returns:
        The minimax score of *board* from *maximising_colour*'s perspective.
    """
    if depth == 0 or is_game_over(board):
        return score(board, maximising_colour)

    moves = legal_moves(board, colour)
    if not moves:
        # Current player must pass; opponent plays next at same depth
        return _minimax(board, opponent(colour), maximising_colour, depth - 1)

    if colour == maximising_colour:
        best = float("-inf")
        for sq in moves:
            new_board = apply_move(board, colour, sq)
            val = _minimax(new_board, opponent(colour), maximising_colour, depth - 1)
            best = max(best, val)
        return int(best)
    else:
        best = float("inf")
        for sq in moves:
            new_board = apply_move(board, colour, sq)
            val = _minimax(new_board, opponent(colour), maximising_colour, depth - 1)
            best = min(best, val)
        return int(best)
