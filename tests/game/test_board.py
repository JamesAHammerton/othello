from game.board import INITIAL_SQUARES, Board


class TestBoardInit:
    def test_initial_pieces_placed(self):
        board = Board()
        for square, colour in INITIAL_SQUARES.items():
            assert board.get(square) == colour

    def test_initial_piece_count(self):
        board = Board()
        white, black = board.piece_counts()
        assert white == 2
        assert black == 2


class TestBoardGet:
    def test_get_occupied_square(self):
        board = Board()
        assert board.get((3, 3)) == "white"

    def test_get_empty_square_returns_none(self):
        board = Board()
        assert board.get((0, 0)) is None


class TestBoardPlace:
    def test_place_piece(self):
        board = Board.empty()
        board.place((0, 0), "black")
        assert board.get((0, 0)) == "black"

    def test_place_overwrites_existing(self):
        board = Board.empty()
        board.place((0, 0), "black")
        board.place((0, 0), "white")
        assert board.get((0, 0)) == "white"


class TestBoardRemove:
    def test_remove_piece(self):
        board = Board()
        board.remove((3, 3))
        assert board.get((3, 3)) is None

    def test_remove_empty_square_is_noop(self):
        board = Board.empty()
        board.remove((0, 0))  # should not raise
        assert board.get((0, 0)) is None


class TestBoardCopy:
    def test_copy_is_independent(self):
        board = Board()
        copy = board.copy()
        copy.place((0, 0), "black")
        assert board.get((0, 0)) is None


class TestBoardPieceCounts:
    def test_initial_counts(self):
        board = Board()
        white, black = board.piece_counts()
        assert white == 2
        assert black == 2
