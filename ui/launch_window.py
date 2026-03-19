from PySide6.QtWidgets import QMainWindow


class LaunchWindow(QMainWindow):
    """Initial window shown when the application starts.

    Presents three buttons: Play as White, Play as Black, and Quit.
    """

    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError

    def _on_play_white(self) -> None:
        """Start a game where the human plays as White."""
        raise NotImplementedError

    def _on_play_black(self) -> None:
        """Start a game where the human plays as Black."""
        raise NotImplementedError

    def _on_quit(self) -> None:
        """Quit the application."""
        raise NotImplementedError
