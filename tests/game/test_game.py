import pytest

from game.game import Game


class TestGameInit:
    def test_turn_count_starts_at_zero(self):
        raise NotImplementedError

    def test_human_and_computer_colours_assigned(self):
        raise NotImplementedError

    def test_black_goes_first(self):
        raise NotImplementedError


class TestGameScore:
    def test_initial_score_is_two_two(self):
        raise NotImplementedError


class TestGameApplyMove:
    def test_turn_count_increments(self):
        raise NotImplementedError

    def test_illegal_move_raises(self):
        raise NotImplementedError

    def test_current_player_advances(self):
        raise NotImplementedError


class TestGamePassTurn:
    def test_pass_increments_turn_count(self):
        raise NotImplementedError

    def test_pass_advances_player(self):
        raise NotImplementedError


class TestGameIsOver:
    def test_not_over_at_start(self):
        raise NotImplementedError
