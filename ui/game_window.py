
from PySide6.QtWidgets import QMainWindow

from game.board import Colour, Square
from game.game import Game
from ui.board_widget import BoardWidget
from ui.side_panel import SidePanel


class GameWindow(QMainWindow):
    """Game window containing the side panel and board widget.

    Orchestrates the turn loop: human input, computer moves, highlights,
    pass detection, and end-of-game handling.
    """

    def __init__(self, human_colour: Colour) -> None:
        """Create and show a game with the human playing *human_colour*.

        Args:
            human_colour: "white" or "black".
        """
        super().__init__()
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Turn loop
    # ------------------------------------------------------------------

    def _start_turn(self) -> None:
        """Begin the next turn: check for game-over, pass, or activate input."""
        raise NotImplementedError

    def _handle_square_clicked(self, square: Square) -> None:
        """Called when the human clicks a square on the board.

        Highlights green (legal) or red (illegal) then delegates to
        ``_handle_move`` or returns to waiting state.
        """
        raise NotImplementedError

    def _handle_move(self, square: Square) -> None:
        """Highlight *square* bright green then schedule ``_apply_move``."""
        raise NotImplementedError

    def _apply_move(self) -> None:
        """Apply the pending move to the game, refresh the UI, start next turn."""
        raise NotImplementedError

    def _handle_computer_move(self, square: Square) -> None:
        """Slot called when ``ComputerWorker`` emits ``move_ready``."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Popups
    # ------------------------------------------------------------------

    def _show_pass_popup(self, is_human: bool) -> None:
        """Show a modal dialog explaining that the current player must pass.

        Args:
            is_human: True if the passing player is the human.
        """
        raise NotImplementedError

    def _show_game_over_popup(self) -> None:
        """Show a modal dialog announcing the end of the game."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _on_finish(self) -> None:
        """Close this window and return to the launch window."""
        raise NotImplementedError
