import pytest

from ai.levels import (
    DEFAULT_LEVEL,
    LEVEL_ORDER,
    PlayerLevel,
    choose_move,
    next_level,
)
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
