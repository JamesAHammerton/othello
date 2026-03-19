from game.board import Board, Colour, Square


def best_move(board: Board, colour: Colour, depth: int = 4) -> Square:
    """Return the best move for *colour* using minimax search to *depth*.

    Ties in score are broken by random selection among the tied moves.

    Raises ValueError if there are no legal moves for *colour*.
    """
    raise NotImplementedError


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
    raise NotImplementedError
