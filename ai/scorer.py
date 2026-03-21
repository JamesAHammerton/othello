from game.board import Board, Colour
from game.rules import C_SQUARES, CORNERS, legal_moves, opponent

# Squares diagonally adjacent to each corner — holding these is disadvantageous
# because it gives the opponent a path to the corner.
DIAGONAL_CORNERS: list[tuple[int, int]] = [(1, 1), (6, 1), (1, 6), (6, 6)]


def score_naive(board: Board, colour: Colour) -> int:
    """Score by raw piece count differential only."""
    white_count, black_count = board.piece_counts()
    colour_pieces = white_count if colour == "white" else black_count
    opp_pieces = black_count if colour == "white" else white_count
    return colour_pieces - opp_pieces


def score_amateur(board: Board, colour: Colour) -> int:
    """Score with piece count, corner bonus, and X-square penalty.

    Formula:
        piece_diff
        + 10 * (own_corners - opp_corners)
        + 10 * (opp_x_squares - own_x_squares)
    """
    opp = opponent(colour)
    piece_diff = score_naive(board, colour)

    colour_corners = sum(1 for sq in CORNERS if board.get(sq) == colour)
    opp_corners = sum(1 for sq in CORNERS if board.get(sq) == opp)
    corner_diff = colour_corners - opp_corners

    colour_diag = sum(1 for sq in DIAGONAL_CORNERS if board.get(sq) == colour)
    opp_diag = sum(1 for sq in DIAGONAL_CORNERS if board.get(sq) == opp)
    diagonal_penalty = opp_diag - colour_diag

    return piece_diff + 10 * corner_diff + 10 * diagonal_penalty


def score_experienced(board: Board, colour: Colour) -> int:
    """Score with amateur formula plus C-square penalty.

    Formula:
        score_amateur + 5 * (opp_c_squares - own_c_squares)
    """
    opp = opponent(colour)
    colour_c = sum(1 for sq in C_SQUARES if board.get(sq) == colour)
    opp_c = sum(1 for sq in C_SQUARES if board.get(sq) == opp)
    c_penalty = opp_c - colour_c
    return score_amateur(board, colour) + 5 * c_penalty


def score_expert(board: Board, colour: Colour) -> int:
    """Score with experienced formula plus mobility term.

    Formula:
        score_experienced + 1 * (own_legal_moves - opp_legal_moves)
    """
    opp = opponent(colour)
    own_mobility = len(legal_moves(board, colour))
    opp_mobility = len(legal_moves(board, opp))
    return score_experienced(board, colour) + (own_mobility - opp_mobility)


# Alias kept for backward compatibility with existing minimax code.
score = score_amateur
