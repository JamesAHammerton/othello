from unittest.mock import patch

import pytest

from ai.minimax import _best_move_alpha_beta, best_move
from ai.scorer import score_amateur
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


class TestBestMoveAlphaBeta:
    def test_returns_legal_move(self):
        board = Board()
        move = _best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)
        from game.rules import legal_moves

        assert move in legal_moves(board, "black")

    def test_no_legal_moves_raises(self):
        board = Board.empty()
        for col in range(8):
            for row in range(8):
                board.place((col, row), "white")
        with pytest.raises(ValueError, match="No legal moves"):
            _best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)

    def test_same_result_as_minimax(self):
        # Alpha-beta is an optimisation — must produce the same result as minimax.
        board = Board.empty()
        board.place((1, 0), "black")
        board.place((2, 0), "white")
        board.place((0, 3), "black")
        board.place((0, 4), "black")
        board.place((0, 5), "white")

        with patch("random.choice", side_effect=lambda x: x[0]):
            ab_move = _best_move_alpha_beta(
                board, "white", depth=1, scorer=score_amateur
            )
            mm_move = best_move(board, "white", depth=1)

        assert ab_move == mm_move

    def test_respects_random_tiebreaking(self):
        board = Board()
        # Mock random.choice to always return the last element
        with patch("random.choice", side_effect=lambda x: x[-1]) as mock_choice:
            _best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)
            mock_choice.assert_called_once()

    def test_deeper_search_matches_minimax(self):
        # Verify equivalence at depth 3 on an asymmetric board.
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))

        with patch("random.choice", side_effect=lambda x: x[0]):
            ab_move = _best_move_alpha_beta(
                board, "white", depth=3, scorer=score_amateur
            )
            mm_move = best_move(board, "white", depth=3)

        assert ab_move == mm_move
