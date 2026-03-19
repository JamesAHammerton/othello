import pytest

from game.board import Board
from game.rules import legal_moves, flipped_squares, apply_move, is_game_over, opponent


class TestOpponent:
    def test_opponent_of_white(self):
        raise NotImplementedError

    def test_opponent_of_black(self):
        raise NotImplementedError


class TestLegalMoves:
    def test_initial_black_has_four_moves(self):
        raise NotImplementedError

    def test_initial_white_has_four_moves(self):
        raise NotImplementedError

    def test_no_legal_moves_on_full_board(self):
        raise NotImplementedError


class TestFlippedSquares:
    def test_flips_correct_squares(self):
        raise NotImplementedError

    def test_illegal_move_returns_empty(self):
        raise NotImplementedError


class TestApplyMove:
    def test_piece_placed_at_square(self):
        raise NotImplementedError

    def test_opponent_pieces_flipped(self):
        raise NotImplementedError

    def test_illegal_move_raises(self):
        raise NotImplementedError

    def test_original_board_unchanged(self):
        raise NotImplementedError


class TestIsGameOver:
    def test_initial_board_not_over(self):
        raise NotImplementedError

    def test_full_board_is_over(self):
        raise NotImplementedError

    def test_no_moves_for_either_player_is_over(self):
        raise NotImplementedError
