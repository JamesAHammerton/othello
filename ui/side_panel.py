from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class SidePanel(QWidget):
    """Left-hand panel displaying score, turn count, and the Finish button.

    The Finish button is hidden until ``show_finish_button()`` is called.
    """

    finish_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self._score_label = QLabel("Score: 2 / 2")
        self._turns_label = QLabel("Turns: 0")
        self._finish_btn = QPushButton("Finish")
        self._finish_btn.setVisible(False)
        self._finish_btn.clicked.connect(self._on_finish_clicked)

        layout.addWidget(self._score_label)
        layout.addWidget(self._turns_label)
        layout.addStretch()
        layout.addWidget(self._finish_btn)

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
