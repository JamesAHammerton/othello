from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from ai.levels import LEVEL_CONFIGS, PlayerLevel
from game.board import Colour


class SidePanel(QWidget):
    """Left-hand panel displaying level info, player colours, score, turn count,
    and the Finish button.

    The Finish button is hidden until ``show_finish_button()`` is called.
    """

    finish_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self._level_name_label = QLabel()
        self._level_desc_label = QLabel()
        self._white_label = QLabel()
        self._black_label = QLabel()
        self._score_label = QLabel("Score: 2 / 2")
        self._turns_label = QLabel("Turns: 0")
        self._finish_btn = QPushButton("Finish")
        self._finish_btn.setVisible(False)
        self._finish_btn.clicked.connect(self._on_finish_clicked)

        layout.addWidget(self._level_name_label)
        layout.addWidget(self._level_desc_label)
        layout.addWidget(self._white_label)
        layout.addWidget(self._black_label)
        layout.addWidget(self._score_label)
        layout.addWidget(self._turns_label)
        layout.addStretch()
        layout.addWidget(self._finish_btn)

    def set_level(self, level: PlayerLevel) -> None:
        """Update the level name and strategy description labels."""
        config = LEVEL_CONFIGS[level]
        self._level_name_label.setText(f"Level: {config.name}")
        self._level_desc_label.setText(f"  {config.description}")

    def set_players(self, human_colour: Colour) -> None:
        """Populate the white/black identity labels from the human's colour."""
        if human_colour == "white":
            self._white_label.setText("White: Human")
            self._black_label.setText("Black: Computer")
        else:
            self._white_label.setText("White: Computer")
            self._black_label.setText("Black: Human")

    def update_score(self, white: int, black: int) -> None:
        """Update the score label to show *white* / *black*."""
        self._score_label.setText(f"Score: {white} / {black}")

    def update_turns(self, count: int) -> None:
        """Update the turn counter label to *count*."""
        self._turns_label.setText(f"Turns: {count}")

    def show_finish_button(self) -> None:
        """Make the Finish button visible (called when the game ends)."""
        self._finish_btn.setVisible(True)

    def _on_finish_clicked(self) -> None:
        """Emit ``finish_clicked`` signal."""
        self.finish_clicked.emit()
