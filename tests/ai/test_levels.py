from unittest.mock import patch

import pytest

from ai.levels import (
    DEFAULT_LEVEL,
    LEVEL_ORDER,
    PlayerLevel,
    choose_move,
    next_level,
)
from ai.scorer import score_amateur, score_naive
from game.board import Board
from game.rules import legal_moves


class TestLevelOrder:
    def test_has_five_entries(self):
        assert len(LEVEL_ORDER) == 5

    def test_correct_order(self):
        assert LEVEL_ORDER == [
            PlayerLevel.DUMB,
            PlayerLevel.NAIVE,
            PlayerLevel.AMATEUR,
            PlayerLevel.EXPERIENCED,
            PlayerLevel.EXPERT,
        ]


class TestDefaultLevel:
    def test_default_is_amateur(self):
        assert DEFAULT_LEVEL == PlayerLevel.AMATEUR


class TestNextLevel:
    def test_cycles_forward(self):
        assert next_level(PlayerLevel.DUMB) == PlayerLevel.NAIVE
        assert next_level(PlayerLevel.NAIVE) == PlayerLevel.AMATEUR
        assert next_level(PlayerLevel.AMATEUR) == PlayerLevel.EXPERIENCED
        assert next_level(PlayerLevel.EXPERIENCED) == PlayerLevel.EXPERT

    def test_wraps_from_expert_to_dumb(self):
        assert next_level(PlayerLevel.EXPERT) == PlayerLevel.DUMB


class TestChooseMove:
    def _board(self) -> Board:
        return Board()

    def test_dumb_returns_legal_move(self):
        board = self._board()
        move = choose_move(board, "black", PlayerLevel.DUMB)
        assert move in legal_moves(board, "black")

    @pytest.mark.parametrize("level", list(PlayerLevel))
    def test_each_level_returns_legal_move(self, level: PlayerLevel):
        board = self._board()
        move = choose_move(board, "black", level)
        assert move in legal_moves(board, "black")

    def test_no_legal_moves_raises(self):
        board = Board.empty()
        for col in range(8):
            for row in range(8):
                board.place((col, row), "white")
        with pytest.raises(ValueError, match="No legal moves"):
            choose_move(board, "black", PlayerLevel.DUMB)

    def test_naive_uses_score_naive(self):
        board = self._board()
        with patch("ai.levels.best_move", return_value=(2, 3)) as mock_best_move:
            choose_move(board, "black", PlayerLevel.NAIVE)
        assert mock_best_move.call_args.kwargs["scorer"] == score_naive

    def test_amateur_uses_score_amateur(self):
        board = self._board()
        with patch("ai.levels.best_move", return_value=(2, 3)) as mock_best_move:
            choose_move(board, "black", PlayerLevel.AMATEUR)
        assert mock_best_move.call_args.kwargs["scorer"] == score_amateur
