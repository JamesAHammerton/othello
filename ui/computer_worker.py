from PySide6.QtCore import QObject, QRunnable, Signal

from ai.levels import PlayerLevel, choose_move
from game.board import Board, Colour, Square


class WorkerSignals(QObject):
    """Signals emitted by ComputerWorker.

    Must live in a QObject subclass so Qt can route them across threads.
    """

    move_ready = Signal(tuple)  # emits Square = (col, row)


class ComputerWorker(QRunnable):
    """Runs ``ai.levels.choose_move`` on a thread-pool thread.

    Receives an immutable copy of the board so it never touches shared state.
    Emits ``signals.move_ready`` with the chosen square when done.
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
        """Compute the best move and emit ``signals.move_ready``."""
        square: Square = choose_move(self._board, self._colour, self._level)
        self.signals.move_ready.emit(square)
