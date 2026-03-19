from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class SidePanel(QWidget):
    """Left-hand panel displaying score, turn count, and the Finish button.

    The Finish button is hidden until ``show_finish_button()`` is called.
    """

    finish_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        raise NotImplementedError

    def update_score(self, white: int, black: int) -> None:
        """Update the score label to show *white* / *black*."""
        raise NotImplementedError

    def update_turns(self, count: int) -> None:
        """Update the turn counter label to *count*."""
        raise NotImplementedError

    def show_finish_button(self) -> None:
        """Make the Finish button visible (called when the game ends)."""
        raise NotImplementedError

    def _on_finish_clicked(self) -> None:
        """Emit ``finish_clicked`` signal."""
        raise NotImplementedError
