import pytest

from ai.minimax import best_move
from game.board import Board


class TestBestMove:
    def test_returns_legal_move(self):
        board = Board()
        move = best_move(board, "black", depth=1)
        from game.rules import legal_moves

        assert move in legal_moves(board, "black")

    def test_no_legal_moves_raises(self):
        # Board full of white — black has no legal moves
        board = Board.empty()
        for col in range(8):
            for row in range(8):
                board.place((col, row), "white")
        with pytest.raises(ValueError, match="No legal moves"):
            best_move(board, "black")

    def test_takes_winning_corner(self):
        # Position with corner (0,0) and non-corner (0,2) both legal for white.
        # Corner scores +10 from the corner bonus; minimax should choose it.
        board = Board.empty()
        board.place((1, 0), "black")  # black B1
        board.place((2, 0), "white")  # white C1 → enables corner A1=(0,0)
        board.place((0, 3), "black")  # black A4
        board.place((0, 4), "black")  # black A5
        board.place((0, 5), "white")  # white A6 → enables non-corner (0,2)
        # Legal moves for white: (0,0) [corner] and (0,2) [non-corner]
        move = best_move(board, "white", depth=1)
        assert move == (0, 0)
