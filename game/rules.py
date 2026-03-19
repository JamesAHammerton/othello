from game.board import Board, Colour, Square

# Unit vectors for all 8 directions (horizontal, vertical, diagonal).
# Used to cast rays from a candidate square: a move is legal if at least one
# ray crosses one or more opponent pieces and terminates on a friendly piece.
# All opponent pieces along such rays are flipped when the move is played.
DIRECTIONS: list[tuple[int, int]] = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

CORNERS: list[Square] = [(0, 0), (7, 0), (0, 7), (7, 7)]


def legal_moves(board: Board, colour: Colour) -> list[Square]:
    """Return all squares where *colour* can legally place a piece."""
    raise NotImplementedError


def flipped_squares(board: Board, colour: Colour, square: Square) -> list[Square]:
    """Return the list of opponent squares that would be flipped by placing
    *colour* at *square*.  Returns an empty list if the move is illegal."""
    raise NotImplementedError


def apply_move(board: Board, colour: Colour, square: Square) -> Board:
    """Return a new Board reflecting the state after *colour* places at *square*.

    Raises ValueError if the move is illegal.
    """
    raise NotImplementedError


def is_game_over(board: Board) -> bool:
    """Return True if neither player has a legal move (game is finished)."""
    raise NotImplementedError


def opponent(colour: Colour) -> Colour:
    """Return the opposite colour."""
    raise NotImplementedError
