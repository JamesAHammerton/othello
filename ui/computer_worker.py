
from PySide6.QtCore import QObject, QRunnable, Signal

from game.board import Board, Colour, Square


class WorkerSignals(QObject):
    """Signals emitted by ComputerWorker.

    Must live in a QObject subclass so Qt can route them across threads.
    """

    move_ready = Signal(tuple)  # emits Square = (col, row)


class ComputerWorker(QRunnable):
    """Runs ``ai.minimax.best_move`` on a thread-pool thread.

    Receives an immutable copy of the board so it never touches shared state.
    Emits ``signals.move_ready`` with the chosen square when done.
    """

    def __init__(self, board: Board, colour: Colour) -> None:
        """
        Args:
            board: A copy of the current board state (not shared with UI thread).
            colour: The colour the computer is playing.
        """
        super().__init__()
        raise NotImplementedError

    def run(self) -> None:
        """Compute the best move and emit ``signals.move_ready``."""
        raise NotImplementedError
