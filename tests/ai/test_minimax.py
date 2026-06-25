from unittest.mock import patch

import pytest

from ai.minimax import _alpha_beta, _minimax, best_move, best_move_alpha_beta
from ai.scorer import score_amateur, score_naive
from game.board import Board
from game.rules import apply_move


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
        move = best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)
        from game.rules import legal_moves

        assert move in legal_moves(board, "black")

    def test_no_legal_moves_raises(self):
        board = Board.empty()
        for col in range(8):
            for row in range(8):
                board.place((col, row), "white")
        with pytest.raises(ValueError, match="No legal moves"):
            best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)

    def test_same_result_as_minimax(self):
        # Alpha-beta is an optimisation — must produce the same result as minimax.
        board = Board.empty()
        board.place((1, 0), "black")
        board.place((2, 0), "white")
        board.place((0, 3), "black")
        board.place((0, 4), "black")
        board.place((0, 5), "white")

        with patch("random.choice", side_effect=lambda x: x[0]):
            ab_move = best_move_alpha_beta(
                board, "white", depth=1, scorer=score_amateur
            )
            mm_move = best_move(board, "white", depth=1)

        assert ab_move == mm_move

    def test_respects_random_tiebreaking(self):
        board = Board()
        # Mock random.choice to always return the last element
        with patch("random.choice", side_effect=lambda x: x[-1]) as mock_choice:
            best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)
            mock_choice.assert_called_once()

    def test_deeper_search_matches_minimax(self):
        # Verify equivalence at depth 3 on an asymmetric board.
        board = Board()
        from game.rules import apply_move

        board = apply_move(board, "black", (2, 3))

        with patch("random.choice", side_effect=lambda x: x[0]):
            ab_move = best_move_alpha_beta(
                board, "white", depth=3, scorer=score_amateur
            )
            mm_move = best_move(board, "white", depth=3)

        assert ab_move == mm_move


def _pass_does_not_skip_a_real_ply_board() -> Board:
    """Board where white has two independent moves, and after playing
    either one, black is forced to pass leaving white free to play the
    other.

    Layout (boundary column avoids the symmetric reverse-flank that would
    otherwise also give black a move):
        white(0,0) black(1,0) empty(2,0)
        white(0,3) black(1,3) empty(2,3)
    """
    board = Board.empty()
    board.place((0, 3), "white")
    board.place((1, 3), "black")
    board.place((0, 0), "white")
    board.place((1, 0), "black")
    return board


class TestForcedPassPreservesDepth:
    """ISSUE-2: a forced pass must not consume a level of search depth."""

    def test_minimax_explores_ply_after_forced_pass(self):
        board = _pass_does_not_skip_a_real_ply_board()
        after_first_move = apply_move(board, "white", (2, 3))

        # At this node black must pass and white still has a real move
        # ((2, 0)) available; a correct depth=1 search from here must
        # explore that move rather than evaluating immediately.
        value = _minimax(after_first_move, "black", "white", 1, score_naive)
        white_count, black_count = apply_move(
            after_first_move, "white", (2, 0)
        ).piece_counts()
        assert value == white_count - black_count

    def test_alpha_beta_explores_ply_after_forced_pass(self):
        board = _pass_does_not_skip_a_real_ply_board()
        after_first_move = apply_move(board, "white", (2, 3))

        value = _alpha_beta(
            after_first_move,
            "black",
            "white",
            1,
            float("-inf"),
            float("inf"),
            score_naive,
        )
        white_count, black_count = apply_move(
            after_first_move, "white", (2, 0)
        ).piece_counts()
        assert value == white_count - black_count


class TestAlphaBetaTieBreakingPool:
    """ISSUE-3: root scores must be exact so tie-breaking is unbiased."""

    def test_root_scores_are_exact_not_pruned(self):
        # Two distinct, non-cutoff-triggering root moves on a small custom
        # board; alpha tightened across siblings would otherwise cause the
        # second move searched to be returned with a pruned (inexact) score.
        board = Board()
        moves = []

        def fake_alpha_beta(
            board, colour, maximising_colour, depth, alpha, beta, scorer
        ):
            moves.append(alpha)
            return 0

        with patch("ai.minimax._alpha_beta", side_effect=fake_alpha_beta):
            best_move_alpha_beta(board, "black", depth=1, scorer=score_amateur)

        # Every sibling at the root must be searched with a fresh window,
        # not with alpha tightened by a previous sibling's score.
        assert all(a == float("-inf") for a in moves)
