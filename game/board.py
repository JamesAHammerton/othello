from typing import Literal

Colour = Literal["white", "black"]
Square = tuple[int, int]  # (col 0-7, row 0-7); A1 = (0, 0), H8 = (7, 7)

INITIAL_SQUARES: dict[Square, Colour] = {
    (3, 3): "white",
    (4, 4): "white",
    (3, 4): "black",
    (4, 3): "black",
}


class Board:
    """8x8 Othello board.

    Internally stores pieces as a dict mapping Square -> Colour.
    Squares not in the dict are empty.
    """

    def __init__(self) -> None:
        """Create a board in the standard Othello starting position."""
        self._squares: dict[Square, Colour] = dict(INITIAL_SQUARES)

    @classmethod
    def empty(cls) -> "Board":
        """Return a completely empty board (useful for testing)."""
        board = cls.__new__(cls)
        board._squares = {}
        return board

    def get(self, square: Square) -> Colour | None:
        """Return the colour of the piece at *square*, or None if empty."""
        return self._squares.get(square)

    def place(self, square: Square, colour: Colour) -> None:
        """Place (or replace) a piece of *colour* at *square* in-place."""
        self._squares[square] = colour

    def remove(self, square: Square) -> None:
        """Remove any piece at *square* in-place."""
        self._squares.pop(square, None)

    def copy(self) -> "Board":
        """Return a deep copy of this board."""
        board = Board.__new__(Board)
        board._squares = dict(self._squares)
        return board

    def piece_counts(self) -> tuple[int, int]:
        """Return (white_count, black_count)."""
        white = sum(1 for c in self._squares.values() if c == "white")
        black = sum(1 for c in self._squares.values() if c == "black")
        return white, black

    def all_pieces(self) -> list[tuple[Square, Colour]]:
        """Return a list of (square, colour) for every occupied square."""
        return list(self._squares.items())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return self._squares == other._squares

    def __repr__(self) -> str:
        return f"Board({self._squares!r})"
