from game.board import Board, Colour
from game.rules import CORNERS, opponent

# Squares diagonally adjacent to each corner — holding these is disadvantageous
# because it gives the opponent a path to the corner.
DIAGONAL_CORNERS: list[tuple[int, int]] = [(1, 1), (6, 1), (1, 6), (6, 6)]


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
    opp = opponent(colour)
    white_count, black_count = board.piece_counts()
    colour_pieces = white_count if colour == "white" else black_count
    opp_pieces = black_count if colour == "white" else white_count
    piece_diff = colour_pieces - opp_pieces

    colour_corners = sum(1 for sq in CORNERS if board.get(sq) == colour)
    opp_corners = sum(1 for sq in CORNERS if board.get(sq) == opp)
    corner_diff = colour_corners - opp_corners

    colour_diag = sum(1 for sq in DIAGONAL_CORNERS if board.get(sq) == colour)
    opp_diag = sum(1 for sq in DIAGONAL_CORNERS if board.get(sq) == opp)
    diagonal_penalty = opp_diag - colour_diag

    return piece_diff + 10 * corner_diff + 10 * diagonal_penalty
