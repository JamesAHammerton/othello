import pytest

from game.board import Board
from game.rules import (
    C_SQUARES,
    apply_move,
    flipped_squares,
    is_game_over,
    legal_moves,
    opponent,
)


class TestCSquares:
    def test_has_eight_elements(self):
        assert len(C_SQUARES) == 8

    def test_contains_correct_squares(self):
        expected = {(1, 0), (0, 1), (6, 0), (7, 1), (1, 7), (0, 6), (6, 7), (7, 6)}
        assert set(C_SQUARES) == expected

    def test_no_overlap_with_corners(self):
        from game.rules import CORNERS

        assert not set(C_SQUARES) & set(CORNERS)


class TestOpponent:
    def test_opponent_of_white(self):
        assert opponent("white") == "black"

    def test_opponent_of_black(self):
        assert opponent("black") == "white"


class TestLegalMoves:
    def test_initial_black_has_four_moves(self):
        board = Board()
        moves = legal_moves(board, "black")
        assert len(moves) == 4

    def test_initial_white_has_four_moves(self):
        board = Board()
        moves = legal_moves(board, "white")
        assert len(moves) == 4

    def test_no_legal_moves_on_full_board(self):
        board = Board.empty()
        for col in range(8):
            for row in range(8):
                board.place((col, row), "white")
        assert legal_moves(board, "black") == []


class TestFlippedSquares:
    def test_flips_correct_squares(self):
        board = Board()
        # Black plays at C4=(2,3): flanks white at D4=(3,3) toward E4=(4,3) black
        flips = flipped_squares(board, "black", (2, 3))
        assert (3, 3) in flips

    def test_illegal_move_returns_empty(self):
        board = Board()
        # Occupied square is illegal
        assert flipped_squares(board, "black", (3, 3)) == []


class TestApplyMove:
    def test_piece_placed_at_square(self):
        board = Board()
        new_board = apply_move(board, "black", (2, 3))
        assert new_board.get((2, 3)) == "black"

    def test_opponent_pieces_flipped(self):
        board = Board()
        # Black plays C4=(2,3): white at D4=(3,3) should flip to black
        new_board = apply_move(board, "black", (2, 3))
        assert new_board.get((3, 3)) == "black"

    def test_illegal_move_raises(self):
        board = Board()
        with pytest.raises(ValueError, match="Illegal move"):
            apply_move(board, "black", (0, 0))

    def test_original_board_unchanged(self):
        board = Board()
        original_colour = board.get((3, 3))
        apply_move(board, "black", (2, 3))
        assert board.get((3, 3)) == original_colour


class TestIsGameOver:
    def test_initial_board_not_over(self):
        board = Board()
        assert not is_game_over(board)

    def test_full_board_is_over(self):
        board = Board.empty()
        for col in range(8):
            for row in range(8):
                board.place((col, row), "white")
        assert is_game_over(board)

    def test_no_moves_for_either_player_is_over(self):
        # Board with a single white piece — black has no moves anywhere
        board = Board.empty()
        board.place((0, 0), "white")
        # No black pieces → no flanking possible → neither player can move
        assert is_game_over(board)
