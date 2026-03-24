from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from game.board import Board, Square

# Highlight state constants
HIGHLIGHT_NONE = "none"
HIGHLIGHT_LEGAL = "legal"  # bright green — chosen move about to be placed
HIGHLIGHT_ILLEGAL = "illegal"  # red — illegal human selection

_LABEL_MARGIN = 24  # px reserved for axis labels
_GRID_PEN_WIDTH = 2  # px for grid lines

_COLOR_EMPTY = QColor(200, 200, 200)
_COLOR_LEGAL_MOVE = QColor(144, 238, 144)  # light green
_COLOR_HIGHLIGHT_LEGAL = QColor(0, 200, 0)  # bright green
_COLOR_HIGHLIGHT_ILLEGAL = QColor(220, 0, 0)  # red
_COLOR_GRID = QColor(0, 0, 139)  # dark blue
_COLOR_WHITE_PIECE = QColor(255, 255, 255)
_COLOR_BLACK_PIECE = QColor(0, 0, 0)
_COLOR_PIECE_BORDER = QColor(80, 80, 80)


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
        self._board: Board = Board()
        self._legal_moves: set[Square] = set()
        self._highlight_square: Square | None = None
        self._highlight_type: str = HIGHLIGHT_NONE
        self._interactive: bool = True
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    # ------------------------------------------------------------------
    # Public API (called by GameWindow)
    # ------------------------------------------------------------------

    def set_board(self, board: Board) -> None:
        """Update the displayed board state and repaint."""
        self._board = board
        self.update()

    def set_legal_moves(self, squares: list[Square]) -> None:
        """Mark *squares* as legal moves (shaded light green) and repaint."""
        self._legal_moves = set(squares)
        self.update()

    def set_highlight(self, square: Square, highlight: str) -> None:
        """Highlight a single *square* with the given state and repaint.

        Args:
            square: The square to highlight.
            highlight: One of HIGHLIGHT_LEGAL or HIGHLIGHT_ILLEGAL.
        """
        self._highlight_square = square
        self._highlight_type = highlight
        self.update()

    def clear_highlight(self) -> None:
        """Remove any active single-square highlight and repaint."""
        self._highlight_square = None
        self._highlight_type = HIGHLIGHT_NONE
        self.update()

    def set_interactive(self, enabled: bool) -> None:
        """Enable or disable click interaction (used during computer turns)."""
        self._interactive = enabled

    # ------------------------------------------------------------------
    # Qt overrides
    # ------------------------------------------------------------------

    def sizeHint(self) -> QSize:  # noqa: N802
        sz = self._square_size_px()
        total = _LABEL_MARGIN + 8 * sz
        return QSize(total, total)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self.updateGeometry()

    def paintEvent(self, _event: QPaintEvent) -> None:  # noqa: N802
        """Paint the board, pieces, labels, grid, and highlights."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        sz = self._square_size_px()
        margin = _LABEL_MARGIN

        # Column labels A-H along the top
        for col in range(8):
            label = chr(ord("A") + col)
            x = margin + col * sz + sz // 2 - 4
            painter.drawText(x, margin - 6, label)

        # Row labels 1-8 along the left
        for row in range(8):
            label = str(row + 1)
            y = margin + row * sz + sz // 2 + 5
            painter.drawText(4, y, label)

        # Squares
        for col in range(8):
            for row in range(8):
                sq: Square = (col, row)
                x = margin + col * sz
                y = margin + row * sz

                # Background colour
                if sq == self._highlight_square:
                    if self._highlight_type == HIGHLIGHT_LEGAL:
                        bg = _COLOR_HIGHLIGHT_LEGAL
                    elif self._highlight_type == HIGHLIGHT_ILLEGAL:
                        bg = _COLOR_HIGHLIGHT_ILLEGAL
                    else:
                        bg = _COLOR_EMPTY
                elif sq in self._legal_moves:
                    bg = _COLOR_LEGAL_MOVE
                else:
                    bg = _COLOR_EMPTY
                painter.fillRect(x, y, sz, sz, bg)

                # Piece
                piece = self._board.get(sq)
                if piece is not None:
                    piece_colour = (
                        _COLOR_WHITE_PIECE if piece == "white" else _COLOR_BLACK_PIECE
                    )
                    pad = max(sz // 8, 2)
                    painter.setPen(QPen(_COLOR_PIECE_BORDER, 1))
                    painter.setBrush(piece_colour)
                    painter.drawEllipse(x + pad, y + pad, sz - 2 * pad, sz - 2 * pad)

        # Grid lines
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(_COLOR_GRID, _GRID_PEN_WIDTH)
        painter.setPen(pen)
        for i in range(9):
            x = margin + i * sz
            painter.drawLine(x, margin, x, margin + 8 * sz)
            y = margin + i * sz
            painter.drawLine(margin, y, margin + 8 * sz, y)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Translate a mouse click into a square_clicked signal."""
        if not self._interactive:
            return
        sq = self._square_at(int(event.position().x()), int(event.position().y()))
        if sq is not None:
            self.square_clicked.emit(sq)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _square_size_px(self) -> int:
        """Return the side length of one square in pixels (~1 cm at physical DPI)."""
        screen = self.screen()
        if screen is not None:
            dpi = screen.physicalDotsPerInch()
            px = int(dpi / 2.54)
            if px > 10:
                return px
        return 40  # fallback (~1 cm at 96 DPI)

    def _square_at(self, x: int, y: int) -> Square | None:
        """Return the board square under pixel coordinates *(x, y)*, or None."""
        sz = self._square_size_px()
        margin = _LABEL_MARGIN
        col = (x - margin) // sz
        row = (y - margin) // sz
        if 0 <= col <= 7 and 0 <= row <= 7:
            return (col, row)
        return None
