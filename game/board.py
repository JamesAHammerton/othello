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
    """8×8 Othello board.

    Internally stores pieces as a dict mapping Square -> Colour.
    Squares not in the dict are empty.
    """

    def __init__(self) -> None:
        """Create a board in the standard Othello starting position."""
        raise NotImplementedError

    @classmethod
    def empty(cls) -> "Board":
        """Return a completely empty board (useful for testing)."""
        raise NotImplementedError

    def get(self, square: Square) -> Colour | None:
        """Return the colour of the piece at *square*, or None if empty."""
        raise NotImplementedError

    def place(self, square: Square, colour: Colour) -> None:
        """Place (or replace) a piece of *colour* at *square* in-place."""
        raise NotImplementedError

    def remove(self, square: Square) -> None:
        """Remove any piece at *square* in-place."""
        raise NotImplementedError

    def copy(self) -> "Board":
        """Return a deep copy of this board."""
        raise NotImplementedError

    def piece_counts(self) -> tuple[int, int]:
        """Return (white_count, black_count)."""
        raise NotImplementedError

    def all_pieces(self) -> list[tuple[Square, Colour]]:
        """Return a list of (square, colour) for every occupied square."""
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
