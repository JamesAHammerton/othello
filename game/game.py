from game.board import Board, Colour, Square


class Game:
    """Mutable game-state container consumed by the UI layer.

    Owns the current board, whose turn it is, and the turn counter.
    All rule enforcement is delegated to ``game.rules``.
    """

    def __init__(self, human_colour: Colour) -> None:
        """Initialise a new game.

        Args:
            human_colour: The colour the human player is using.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def board(self) -> Board:
        """The current board state."""
        raise NotImplementedError

    @property
    def current_player(self) -> Colour:
        """The colour whose turn it is."""
        raise NotImplementedError

    @property
    def human_colour(self) -> Colour:
        """The colour assigned to the human player."""
        raise NotImplementedError

    @property
    def computer_colour(self) -> Colour:
        """The colour assigned to the computer player."""
        raise NotImplementedError

    @property
    def turn_count(self) -> int:
        """Number of turns that have been played (0 at game start)."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def score(self) -> tuple[int, int]:
        """Return (white_count, black_count)."""
        raise NotImplementedError

    def legal_moves(self) -> list[Square]:
        """Return legal moves for the current player."""
        raise NotImplementedError

    def is_over(self) -> bool:
        """Return True when the game has ended."""
        raise NotImplementedError

    def is_human_turn(self) -> bool:
        """Return True when it is the human player's turn."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def apply_move(self, square: Square) -> None:
        """Apply *square* as the current player's move and advance the turn.

        Raises ValueError if the move is illegal.
        """
        raise NotImplementedError

    def pass_turn(self) -> None:
        """Pass the current player's turn and advance to the opponent."""
        raise NotImplementedError
