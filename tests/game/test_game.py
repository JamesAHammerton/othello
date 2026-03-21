import pytest

from game.game import Game


class TestGameInit:
    def test_turn_count_starts_at_zero(self):
        game = Game("white")
        assert game.turn_count == 0

    def test_human_and_computer_colours_assigned(self):
        game = Game("white")
        assert game.human_colour == "white"
        assert game.computer_colour == "black"

    def test_black_goes_first(self):
        game = Game("white")
        assert game.current_player == "black"


class TestGameScore:
    def test_initial_score_is_two_two(self):
        game = Game("white")
        white, black = game.score()
        assert white == 2
        assert black == 2


class TestGameApplyMove:
    def test_turn_count_increments(self):
        game = Game("white")
        game.apply_move((2, 3))  # black plays C4
        assert game.turn_count == 1

    def test_illegal_move_raises(self):
        game = Game("white")
        with pytest.raises(ValueError, match="Illegal move"):
            game.apply_move((0, 0))

    def test_current_player_advances(self):
        game = Game("white")
        game.apply_move((2, 3))  # black plays
        assert game.current_player == "white"


class TestGamePassTurn:
    def test_pass_increments_turn_count(self):
        game = Game("white")
        game.pass_turn()
        assert game.turn_count == 1

    def test_pass_advances_player(self):
        game = Game("white")
        assert game.current_player == "black"
        game.pass_turn()
        assert game.current_player == "white"


class TestGameIsOver:
    def test_not_over_at_start(self):
        game = Game("white")
        assert not game.is_over()
