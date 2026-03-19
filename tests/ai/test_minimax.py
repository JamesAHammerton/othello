import pytest

from ai.minimax import best_move
from game.board import Board


class TestBestMove:
    def test_returns_legal_move(self):
        raise NotImplementedError

    def test_no_legal_moves_raises(self):
        raise NotImplementedError

    def test_takes_winning_corner(self):
        raise NotImplementedError
