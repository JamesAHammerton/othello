import pytest

from game.board import INITIAL_SQUARES, Board


class TestBoardInit:
    def test_initial_pieces_placed(self):
        raise NotImplementedError

    def test_initial_piece_count(self):
        raise NotImplementedError


class TestBoardGet:
    def test_get_occupied_square(self):
        raise NotImplementedError

    def test_get_empty_square_returns_none(self):
        raise NotImplementedError


class TestBoardPlace:
    def test_place_piece(self):
        raise NotImplementedError

    def test_place_overwrites_existing(self):
        raise NotImplementedError


class TestBoardRemove:
    def test_remove_piece(self):
        raise NotImplementedError

    def test_remove_empty_square_is_noop(self):
        raise NotImplementedError


class TestBoardCopy:
    def test_copy_is_independent(self):
        raise NotImplementedError


class TestBoardPieceCounts:
    def test_initial_counts(self):
        raise NotImplementedError
