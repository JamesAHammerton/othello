from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)


class LaunchWindow(QMainWindow):
    """Initial window shown when the application starts.

    Presents three buttons: Play as White, Play as Black, and Quit.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Othello")

        central = QWidget()
        layout = QHBoxLayout(central)

        play_white_btn = QPushButton("Play as White")
        play_black_btn = QPushButton("Play as Black")
        quit_btn = QPushButton("Quit")

        play_white_btn.clicked.connect(self._on_play_white)
        play_black_btn.clicked.connect(self._on_play_black)
        quit_btn.clicked.connect(self._on_quit)

        layout.addWidget(play_white_btn)
        layout.addWidget(play_black_btn)
        layout.addWidget(quit_btn)

        self.setCentralWidget(central)

    def _on_play_white(self) -> None:
        """Start a game where the human plays as White."""
        from ui.game_window import GameWindow

        self._game_window = GameWindow("white", self)
        self.hide()

    def _on_play_black(self) -> None:
        """Start a game where the human plays as Black."""
        from ui.game_window import GameWindow

        self._game_window = GameWindow("black", self)
        self.hide()

    def _on_quit(self) -> None:
        """Quit the application."""
        QApplication.quit()
