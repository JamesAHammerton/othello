from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ai.levels import DEFAULT_LEVEL, LEVEL_CONFIGS, PlayerLevel, next_level


class LaunchWindow(QMainWindow):
    """Initial window shown when the application starts.

    Presents level selection, Play as White, Play as Black, and Quit buttons.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Othello")
        self._level: PlayerLevel = DEFAULT_LEVEL

        central = QWidget()
        outer = QVBoxLayout(central)

        # Level selection row
        level_row = QHBoxLayout()
        level_label = QLabel("Level:")
        self._level_btn = QPushButton()
        level_row.addWidget(level_label)
        level_row.addWidget(self._level_btn)
        level_row.addStretch()

        # Play/quit row
        play_row = QHBoxLayout()
        play_white_btn = QPushButton("Play as White")
        play_black_btn = QPushButton("Play as Black")
        quit_btn = QPushButton("Quit")
        play_row.addWidget(play_white_btn)
        play_row.addWidget(play_black_btn)
        play_row.addWidget(quit_btn)

        outer.addLayout(level_row)
        outer.addLayout(play_row)

        self._level_btn.clicked.connect(self._on_cycle_level)
        play_white_btn.clicked.connect(self._on_play_white)
        play_black_btn.clicked.connect(self._on_play_black)
        quit_btn.clicked.connect(self._on_quit)

        play_white_btn.setToolTip(
            "Start a game playing as White (computer plays Black)."
        )
        play_black_btn.setToolTip(
            "Start a game playing as Black (computer plays White)."
        )
        quit_btn.setToolTip("Quit the application.")

        self._update_level_button()
        self.setCentralWidget(central)

    def _update_level_button(self) -> None:
        """Refresh level button text and tooltip from current level config."""
        config = LEVEL_CONFIGS[self._level]
        self._level_btn.setText(config.name)
        self._level_btn.setToolTip(config.description)

    def _on_cycle_level(self) -> None:
        """Advance to the next difficulty level and update the button."""
        self._level = next_level(self._level)
        self._update_level_button()

    def _on_play_white(self) -> None:
        """Start a game where the human plays as White."""
        from ui.game_window import GameWindow

        self._game_window = GameWindow("white", self, self._level)
        self.hide()

    def _on_play_black(self) -> None:
        """Start a game where the human plays as Black."""
        from ui.game_window import GameWindow

        self._game_window = GameWindow("black", self, self._level)
        self.hide()

    def _on_quit(self) -> None:
        """Quit the application."""
        QApplication.quit()
