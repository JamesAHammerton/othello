import pytest

from ai.scorer import score
from game.board import Board


class TestScore:
    def test_equal_board_scores_zero(self):
        raise NotImplementedError

    def test_corner_bonus_applied(self):
        raise NotImplementedError

    def test_diagonal_corner_penalty_applied(self):
        raise NotImplementedError

    def test_piece_difference_counted(self):
        raise NotImplementedError
