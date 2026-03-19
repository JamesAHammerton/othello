from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent, QPaintEvent
from PySide6.QtWidgets import QWidget

from game.board import Board, Square

# Highlight state constants
HIGHLIGHT_NONE = "none"
HIGHLIGHT_LEGAL = "legal"  # bright green — chosen move about to be placed
HIGHLIGHT_ILLEGAL = "illegal"  # red — illegal human selection


class BoardWidget(QWidget):
    """Paints the 8x8 Othello board and emits square_clicked signals.

    Visual states per square:
    - Empty: light grey
    - Legal move for current player: light green
    - Highlighted (chosen move): bright green
    - Highlighted (illegal click): red
    - White piece: white circle
    - Black piece: black circle

    Grid lines: 2px dark blue separating each square.
    Column labels A-H (top), row labels 1-8 (left).
    Square size: ~1 cm x 1 cm based on physical DPI.
    """

    square_clicked = Signal(tuple)  # emits Square = (col, row)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Public API (called by GameWindow)
    # ------------------------------------------------------------------

    def set_board(self, board: Board) -> None:
        """Update the displayed board state and repaint."""
        raise NotImplementedError

    def set_legal_moves(self, squares: list[Square]) -> None:
        """Mark *squares* as legal moves (shaded light green) and repaint."""
        raise NotImplementedError

    def set_highlight(self, square: Square, highlight: str) -> None:
        """Highlight a single *square* with the given state and repaint.

        Args:
            square: The square to highlight.
            highlight: One of HIGHLIGHT_LEGAL or HIGHLIGHT_ILLEGAL.
        """
        raise NotImplementedError

    def clear_highlight(self) -> None:
        """Remove any active single-square highlight and repaint."""
        raise NotImplementedError

    def set_interactive(self, enabled: bool) -> None:
        """Enable or disable click interaction (used during computer turns)."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Qt overrides
    # ------------------------------------------------------------------

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Paint the board, pieces, labels, grid, and highlights."""
        raise NotImplementedError

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Translate a mouse click into a square_clicked signal."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _square_size_px(self) -> int:
        """Return the side length of one square in pixels (~1 cm at physical DPI)."""
        raise NotImplementedError

    def _square_at(self, x: int, y: int) -> Square | None:
        """Return the board square under pixel coordinates *(x, y)*, or None."""
        raise NotImplementedError
