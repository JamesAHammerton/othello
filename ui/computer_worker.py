import logging

from PySide6.QtCore import QObject, QRunnable, Signal

from ai.levels import PlayerLevel, choose_move
from game.board import Board, Colour, Square

logger = logging.getLogger(__name__)


class WorkerSignals(QObject):
    """Signals emitted by ComputerWorker.

    Must live in a QObject subclass so Qt can route them across threads.
    """

    move_ready = Signal(tuple)  # emits Square = (col, row)
    move_failed = Signal(str)  # emits an error message


class ComputerWorker(QRunnable):
    """Runs ``ai.levels.choose_move`` on a thread-pool thread.

    Receives an immutable copy of the board so it never touches shared state.
    Emits ``signals.move_ready`` with the chosen square when done, or
    ``signals.move_failed`` if ``choose_move`` raises.
    """

    def __init__(self, board: Board, colour: Colour, level: PlayerLevel) -> None:
        """
        Args:
            board: A copy of the current board state (not shared with UI thread).
            colour: The colour the computer is playing.
            level: The AI difficulty level to use.
        """
        super().__init__()
        self._board = board
        self._colour = colour
        self._level = level
        self.signals = WorkerSignals()

    def run(self) -> None:
        """Compute the best move and emit ``signals.move_ready``.

        ``QRunnable`` silently drops exceptions raised in ``run()``, so any
        failure must be caught here and reported via ``signals.move_failed``
        rather than left to propagate.
        """
        try:
            square: Square = choose_move(self._board, self._colour, self._level)
        except Exception as exc:
            logger.exception("Computer move calculation failed")
            self.signals.move_failed.emit(str(exc))
            return
        self.signals.move_ready.emit(square)
