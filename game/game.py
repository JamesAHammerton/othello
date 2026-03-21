from game import rules
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
        self._board = Board()
        self._human_colour = human_colour
        self._computer_colour: Colour = rules.opponent(human_colour)
        self._current_player: Colour = "black"  # black always goes first
        self._turn_count = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def board(self) -> Board:
        """The current board state."""
        return self._board

    @property
    def current_player(self) -> Colour:
        """The colour whose turn it is."""
        return self._current_player

    @property
    def human_colour(self) -> Colour:
        """The colour assigned to the human player."""
        return self._human_colour

    @property
    def computer_colour(self) -> Colour:
        """The colour assigned to the computer player."""
        return self._computer_colour

    @property
    def turn_count(self) -> int:
        """Number of turns that have been played (0 at game start)."""
        return self._turn_count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def score(self) -> tuple[int, int]:
        """Return (white_count, black_count)."""
        return self._board.piece_counts()

    def legal_moves(self) -> list[Square]:
        """Return legal moves for the current player."""
        return rules.legal_moves(self._board, self._current_player)

    def is_over(self) -> bool:
        """Return True when the game has ended."""
        return rules.is_game_over(self._board)

    def is_human_turn(self) -> bool:
        """Return True when it is the human player's turn."""
        return self._current_player == self._human_colour

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def apply_move(self, square: Square) -> None:
        """Apply *square* as the current player's move and advance the turn.

        Raises ValueError if the move is illegal.
        """
        self._board = rules.apply_move(self._board, self._current_player, square)
        self._turn_count += 1
        self._current_player = rules.opponent(self._current_player)

    def pass_turn(self) -> None:
        """Pass the current player's turn and advance to the opponent."""
        self._turn_count += 1
        self._current_player = rules.opponent(self._current_player)
