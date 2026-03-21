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


def opponent(colour: Colour) -> Colour:
    """Return the opposite colour."""
    return "black" if colour == "white" else "white"


def flipped_squares(board: Board, colour: Colour, square: Square) -> list[Square]:
    """Return the list of opponent squares that would be flipped by placing
    *colour* at *square*.  Returns an empty list if the move is illegal."""
    if board.get(square) is not None:
        return []
    opp = opponent(colour)
    col, row = square
    flipped: list[Square] = []
    for dc, dr in DIRECTIONS:
        c, r = col + dc, row + dr
        candidates: list[Square] = []
        while 0 <= c <= 7 and 0 <= r <= 7 and board.get((c, r)) == opp:
            candidates.append((c, r))
            c += dc
            r += dr
        if candidates and 0 <= c <= 7 and 0 <= r <= 7 and board.get((c, r)) == colour:
            flipped.extend(candidates)
    return flipped


def legal_moves(board: Board, colour: Colour) -> list[Square]:
    """Return all squares where *colour* can legally place a piece."""
    moves: list[Square] = []
    for col in range(8):
        for row in range(8):
            sq: Square = (col, row)
            if board.get(sq) is None and flipped_squares(board, colour, sq):
                moves.append(sq)
    return moves


def apply_move(board: Board, colour: Colour, square: Square) -> Board:
    """Return a new Board reflecting the state after *colour* places at *square*.

    Raises ValueError if the move is illegal.
    """
    flips = flipped_squares(board, colour, square)
    if not flips:
        raise ValueError(f"Illegal move: {colour} cannot play at {square}")
    new_board = board.copy()
    new_board.place(square, colour)
    for sq in flips:
        new_board.place(sq, colour)
    return new_board


def is_game_over(board: Board) -> bool:
    """Return True if neither player has a legal move (game is finished)."""
    return not legal_moves(board, "white") and not legal_moves(board, "black")
