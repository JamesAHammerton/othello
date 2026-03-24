import random

from ai.scorer import Scorer, score_amateur
from game.board import Board, Colour, Square
from game.rules import apply_move, is_game_over, legal_moves, opponent


def best_move(
    board: Board, colour: Colour, depth: int = 4, scorer: Scorer = score_amateur
) -> Square:
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
        s = _minimax(new_board, opponent(colour), colour, depth - 1, scorer)
        scored.append((s, sq))

    best_score = max(s for s, _ in scored)
    best_moves = [sq for s, sq in scored if s == best_score]
    return random.choice(best_moves)


def _minimax(
    board: Board,
    colour: Colour,
    maximising_colour: Colour,
    depth: int,
    scorer: Scorer,
) -> int:
    """Recursive minimax helper.

    Args:
        board: Current board state.
        colour: The player whose turn it is at this node.
        maximising_colour: The root player (whose perspective we score from).
        depth: Remaining search depth.
        scorer: Evaluation function ``(board, colour) -> int``.

    Returns:
        The minimax score of *board* from *maximising_colour*'s perspective.
    """
    if depth == 0 or is_game_over(board):
        return scorer(board, maximising_colour)

    moves = legal_moves(board, colour)
    if not moves:
        # Current player must pass; opponent plays next at same depth
        return _minimax(board, opponent(colour), maximising_colour, depth - 1, scorer)

    if colour == maximising_colour:
        best = float("-inf")
        for sq in moves:
            new_board = apply_move(board, colour, sq)
            val = _minimax(
                new_board, opponent(colour), maximising_colour, depth - 1, scorer
            )
            best = max(best, val)
        return int(best)
    else:
        best = float("inf")
        for sq in moves:
            new_board = apply_move(board, colour, sq)
            val = _minimax(
                new_board, opponent(colour), maximising_colour, depth - 1, scorer
            )
            best = min(best, val)
        return int(best)


def best_move_alpha_beta(
    board: Board,
    colour: Colour,
    depth: int,
    scorer: Scorer,
) -> Square:
    """Return the best move using alpha-beta pruning.

    Applies the same random tie-breaking as ``best_move``.

    Raises ValueError if there are no legal moves for *colour*.
    """
    moves = legal_moves(board, colour)
    if not moves:
        raise ValueError(f"No legal moves for {colour}")

    scored: list[tuple[int, Square]] = []
    alpha = float("-inf")
    for sq in moves:
        new_board = apply_move(board, colour, sq)
        s = _alpha_beta(
            new_board,
            opponent(colour),
            colour,
            depth - 1,
            alpha,
            float("inf"),
            scorer,
        )
        scored.append((s, sq))
        alpha = max(alpha, s)

    best_score = max(s for s, _ in scored)
    best_moves = [sq for s, sq in scored if s == best_score]
    return random.choice(best_moves)


def _alpha_beta(
    board: Board,
    colour: Colour,
    maximising_colour: Colour,
    depth: int,
    alpha: float,
    beta: float,
    scorer: Scorer,
) -> int:
    """Recursive alpha-beta pruning helper.

    Args:
        board: Current board state.
        colour: The player whose turn it is at this node.
        maximising_colour: The root player (whose perspective we score from).
        depth: Remaining search depth.
        alpha: Best score the maximising player can guarantee so far.
        beta: Best score the minimising player can guarantee so far.
        scorer: Evaluation function ``(board, colour) -> int``.

    Returns:
        The alpha-beta score of *board* from *maximising_colour*'s perspective.
    """
    if depth == 0 or is_game_over(board):
        return scorer(board, maximising_colour)

    moves = legal_moves(board, colour)
    if not moves:
        return _alpha_beta(
            board, opponent(colour), maximising_colour, depth - 1, alpha, beta, scorer
        )

    if colour == maximising_colour:
        best = float("-inf")
        for sq in moves:
            new_board = apply_move(board, colour, sq)
            val = _alpha_beta(
                new_board,
                opponent(colour),
                maximising_colour,
                depth - 1,
                alpha,
                beta,
                scorer,
            )
            best = max(best, val)
            alpha = max(alpha, best)
            if alpha >= beta:
                break  # beta cut-off
        return int(best)
    else:
        best = float("inf")
        for sq in moves:
            new_board = apply_move(board, colour, sq)
            val = _alpha_beta(
                new_board,
                opponent(colour),
                maximising_colour,
                depth - 1,
                alpha,
                beta,
                scorer,
            )
            best = min(best, val)
            beta = min(beta, best)
            if alpha >= beta:
                break  # alpha cut-off
        return int(best)
