from ai.scorer import score, score_amateur, score_experienced, score_expert, score_naive
from game.board import Board


class TestScoreNaive:
    def test_equal_board_scores_zero(self):
        board = Board()
        assert score_naive(board, "white") == 0
        assert score_naive(board, "black") == 0

    def test_piece_difference_counted(self):
        board = Board.empty()
        board.place((0, 1), "white")
        board.place((1, 0), "white")
        board.place((2, 0), "black")
        assert score_naive(board, "white") == 1

    def test_no_corner_bonus(self):
        board = Board.empty()
        board.place((0, 0), "white")  # corner
        board.place((1, 0), "black")
        # naive ignores corners — just piece count: 1-1=0
        assert score_naive(board, "white") == 0

    def test_symmetry(self):
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))
        assert score_naive(board, "white") == -score_naive(board, "black")


class TestScoreAmateur:
    def test_equal_board_scores_zero(self):
        board = Board()
        assert score_amateur(board, "white") == 0
        assert score_amateur(board, "black") == 0

    def test_corner_bonus_applied(self):
        board = Board.empty()
        board.place((0, 0), "white")  # corner
        board.place((1, 0), "black")  # non-corner, non-diagonal
        # piece_diff = 0, corner_diff = 1, diagonal_penalty = 0
        assert score_amateur(board, "white") == 10

    def test_diagonal_corner_penalty_applied(self):
        board = Board.empty()
        board.place((1, 1), "white")  # white holds X-square — penalises white
        board.place((0, 2), "black")
        # piece_diff = 0, corner_diff = 0, colour_diag = 1, opp_diag = 0 → penalty = -1
        assert score_amateur(board, "white") == -10

    def test_piece_difference_counted(self):
        board = Board.empty()
        board.place((0, 1), "white")
        board.place((1, 0), "white")
        board.place((2, 0), "black")
        assert score_amateur(board, "white") == 1

    def test_symmetry(self):
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))
        assert score_amateur(board, "white") == -score_amateur(board, "black")


class TestScoreExperienced:
    def test_c_square_penalty_applied(self):
        board = Board.empty()
        board.place((1, 0), "white")  # white holds a C-square
        board.place((0, 2), "black")
        # piece_diff = 0, no corners, no X-squares
        # c_penalty for white: opp_c - own_c = 0 - 1 = -1 → -5
        assert score_experienced(board, "white") == -5

    def test_c_square_penalty_opponent(self):
        board = Board.empty()
        board.place((1, 0), "black")  # black holds a C-square
        board.place((0, 2), "white")
        # from white's perspective: opp_c=1, own_c=0 → +5
        assert score_experienced(board, "white") == 5

    def test_includes_amateur_component(self):
        board = Board.empty()
        board.place((0, 0), "white")  # corner: 50 total (10 amateur + 40 boost)
        board.place((1, 0), "black")  # C-square for black: +5 for white
        # amateur: corner_diff=1 → +10; experienced: extra corner → +40, c_penalty → +5
        assert score_experienced(board, "white") == 55

    def test_symmetry(self):
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))
        assert score_experienced(board, "white") == -score_experienced(board, "black")


class TestScoreExpert:
    def test_mobility_term_added(self):
        # Initial board: equal mobility (4 moves each), so mobility term = 0
        board = Board()
        assert score_expert(board, "white") == score_experienced(board, "white")

    def test_mobility_advantage_reflected(self):
        # After one black move, white typically has more moves than black.
        # No corners occupied so extra corner weight contributes 0.
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))
        from game.rules import legal_moves

        white_moves = len(legal_moves(board, "white"))
        black_moves = len(legal_moves(board, "black"))
        expected_mobility = white_moves - black_moves
        assert (
            score_expert(board, "white")
            == score_experienced(board, "white") + expected_mobility
        )

    def test_symmetry(self):
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))
        assert score_expert(board, "white") == -score_expert(board, "black")


class TestScoreAlias:
    def test_score_is_score_amateur(self):
        assert score is score_amateur
