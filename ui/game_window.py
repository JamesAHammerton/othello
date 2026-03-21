from PySide6.QtCore import QThreadPool, QTimer
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QWidget

from game.board import Colour, Square
from game.game import Game
from ui.board_widget import HIGHLIGHT_ILLEGAL, HIGHLIGHT_LEGAL, BoardWidget
from ui.computer_worker import ComputerWorker
from ui.side_panel import SidePanel


class GameWindow(QMainWindow):
    """Game window containing the side panel and board widget.

    Orchestrates the turn loop: human input, computer moves, highlights,
    pass detection, and end-of-game handling.
    """

    def __init__(self, human_colour: Colour, launch_window: QMainWindow) -> None:
        """Create and show a game with the human playing *human_colour*.

        Args:
            human_colour: "white" or "black".
            launch_window: The LaunchWindow to restore when the game ends.
        """
        super().__init__()
        self._launch_window = launch_window
        self._game = Game(human_colour)
        self._pending_square: Square | None = None

        self._board_widget = BoardWidget()
        self._side_panel = SidePanel()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self._side_panel)
        layout.addWidget(self._board_widget)
        self.setCentralWidget(central)
        self.setWindowTitle("Othello")

        self._board_widget.square_clicked.connect(self._handle_square_clicked)
        self._side_panel.finish_clicked.connect(self._on_finish)

        self._refresh_ui()
        self.show()
        self._start_turn()

    # ------------------------------------------------------------------
    # Turn loop
    # ------------------------------------------------------------------

    def _refresh_ui(self) -> None:
        white, black = self._game.score()
        self._side_panel.update_score(white, black)
        self._side_panel.update_turns(self._game.turn_count)
        self._board_widget.set_board(self._game.board)

    def _start_turn(self) -> None:
        """Begin the next turn: check for game-over, pass, or activate input."""
        if self._game.is_over():
            self._board_widget.set_interactive(False)
            self._board_widget.set_legal_moves([])
            self._show_game_over_popup()
            self._side_panel.show_finish_button()
            return

        moves = self._game.legal_moves()
        if not moves:
            self._board_widget.set_interactive(False)
            self._board_widget.set_legal_moves([])
            self._show_pass_popup(self._game.is_human_turn())
            self._game.pass_turn()
            self._refresh_ui()
            self._start_turn()
            return

        if self._game.is_human_turn():
            self._board_widget.set_legal_moves(moves)
            self._board_widget.set_interactive(True)
        else:
            self._board_widget.set_legal_moves([])
            self._board_widget.set_interactive(False)
            worker = ComputerWorker(self._game.board.copy(), self._game.current_player)
            worker.signals.move_ready.connect(self._handle_computer_move)
            QThreadPool.globalInstance().start(worker)

    def _handle_square_clicked(self, square: Square) -> None:
        """Called when the human clicks a square on the board.

        Highlights green (legal) or red (illegal) then delegates to
        ``_handle_move`` or returns to waiting state.
        """
        moves = self._game.legal_moves()
        if square in moves:
            self._board_widget.set_interactive(False)
            self._board_widget.set_legal_moves([])
            self._handle_move(square)
        else:
            self._board_widget.set_interactive(False)
            self._board_widget.set_highlight(square, HIGHLIGHT_ILLEGAL)

            def restore() -> None:
                self._board_widget.clear_highlight()
                self._board_widget.set_interactive(True)

            QTimer.singleShot(500, restore)

    def _handle_move(self, square: Square) -> None:
        """Highlight *square* bright green then schedule ``_apply_move``."""
        self._pending_square = square
        self._board_widget.set_highlight(square, HIGHLIGHT_LEGAL)
        QTimer.singleShot(500, self._apply_move)

    def _apply_move(self) -> None:
        """Apply the pending move to the game, refresh the UI, start next turn."""
        assert self._pending_square is not None
        self._game.apply_move(self._pending_square)
        self._pending_square = None
        self._board_widget.clear_highlight()
        self._refresh_ui()
        self._start_turn()

    def _handle_computer_move(self, square: Square) -> None:
        """Slot called when ``ComputerWorker`` emits ``move_ready``."""
        self._handle_move(square)

    # ------------------------------------------------------------------
    # Popups
    # ------------------------------------------------------------------

    def _show_pass_popup(self, is_human: bool) -> None:
        """Show a modal dialog explaining that the current player must pass.

        Args:
            is_human: True if the passing player is the human.
        """
        if is_human:
            msg = "No legal move is available. You must pass."
        else:
            msg = "The computer has no legal move and must pass."
        box = QMessageBox(self)
        box.setWindowTitle("Pass")
        box.setText(msg)
        box.exec()

    def _show_game_over_popup(self) -> None:
        """Show a modal dialog announcing the end of the game."""
        white, black = self._game.score()
        if white > black:
            result = f"White wins! ({white} vs {black})"
        elif black > white:
            result = f"Black wins! ({black} vs {white})"
        else:
            result = f"It's a draw! ({white} all)"
        box = QMessageBox(self)
        box.setWindowTitle("Game Over")
        box.setText(f"The game is over. {result}")
        box.exec()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _on_finish(self) -> None:
        """Close this window and return to the launch window."""
        self.close()
        self._launch_window.show()
