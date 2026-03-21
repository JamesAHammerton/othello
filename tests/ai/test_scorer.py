from ai.scorer import score
from game.board import Board


class TestScore:
    def test_equal_board_scores_zero(self):
        # Initial board: 2 white, 2 black, no corners, no diagonal corners held
        board = Board()
        assert score(board, "white") == 0
        assert score(board, "black") == 0

    def test_corner_bonus_applied(self):
        board = Board.empty()
        board.place((0, 0), "white")  # corner
        board.place((1, 0), "black")  # non-corner, non-diagonal
        # piece_diff = 0, corner_diff = 1-0 = 1, diagonal_penalty = 0
        assert score(board, "white") == 10

    def test_diagonal_corner_penalty_applied(self):
        board = Board.empty()
        board.place((1, 1), "white")  # white holds diagonal corner — penalises white
        board.place((0, 2), "black")  # black has a non-special piece
        # piece_diff = 0, corner_diff = 0
        # colour_diag = 1 (white at (1,1)), opp_diag = 0
        # diagonal_penalty = 0 - 1 = -1 → score = -10
        assert score(board, "white") == -10

    def test_piece_difference_counted(self):
        board = Board.empty()
        board.place((0, 1), "white")
        board.place((1, 0), "white")
        board.place((2, 0), "black")
        # white: 2, black: 1 — no corners or diagonal corners
        assert score(board, "white") == 1
