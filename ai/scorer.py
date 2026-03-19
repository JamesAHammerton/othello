from game.board import Board, Colour


def score(board: Board, colour: Colour) -> int:
    """Score *board* from the perspective of *colour*.

    Formula (from requirements):
        piece_diff
        + 10 * corner_diff
        + 10 * diagonal_corner_penalty

    Where:
        piece_diff             = colour's pieces - opponent's pieces
        corner_diff            = corners held by colour - corners held by opponent
        diagonal_corner_penalty = diagonally-adjacent-to-corner squares held by
                                  opponent - those held by colour
    """
    raise NotImplementedError
