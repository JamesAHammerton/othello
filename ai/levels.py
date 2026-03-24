import random
from dataclasses import dataclass
from enum import Enum

from ai.minimax import best_move, best_move_alpha_beta
from ai.scorer import (
    Scorer,
    score_amateur,
    score_experienced,
    score_expert,
    score_naive,
)
from game.board import Board, Colour, Square
from game.rules import legal_moves


class PlayerLevel(Enum):
    DUMB = "dumb"
    NAIVE = "naive"
    AMATEUR = "amateur"
    EXPERIENCED = "experienced"
    EXPERT = "expert"


@dataclass(frozen=True)
class LevelConfig:
    name: str
    description: str
    depth: int
    scorer: Scorer
    use_alpha_beta: bool


LEVEL_CONFIGS: dict[PlayerLevel, LevelConfig] = {
    PlayerLevel.DUMB: LevelConfig(
        name="Dumb",
        description="Plays a random legal move.",
        depth=0,
        scorer=score_naive,
        use_alpha_beta=False,
    ),
    PlayerLevel.NAIVE: LevelConfig(
        name="Naive",
        description="Looks 2 moves ahead using raw piece count.",
        depth=2,
        scorer=score_naive,
        use_alpha_beta=False,
    ),
    PlayerLevel.AMATEUR: LevelConfig(
        name="Amateur",
        description="Looks 4 moves ahead; values corners and avoids X-squares.",
        depth=4,
        scorer=score_amateur,
        use_alpha_beta=False,
    ),
    PlayerLevel.EXPERIENCED: LevelConfig(
        name="Experienced",
        description="Looks 6 moves ahead; also avoids C-squares. Uses alpha-beta.",
        depth=6,
        scorer=score_experienced,
        use_alpha_beta=True,
    ),
    PlayerLevel.EXPERT: LevelConfig(
        name="Expert",
        description=(
            "Looks 8 moves ahead; weights corners heavily and considers mobility."
            " Uses alpha-beta pruning."
        ),
        depth=8,
        scorer=score_expert,
        use_alpha_beta=True,
    ),
}

LEVEL_ORDER: list[PlayerLevel] = [
    PlayerLevel.DUMB,
    PlayerLevel.NAIVE,
    PlayerLevel.AMATEUR,
    PlayerLevel.EXPERIENCED,
    PlayerLevel.EXPERT,
]

DEFAULT_LEVEL: PlayerLevel = PlayerLevel.AMATEUR


def next_level(level: PlayerLevel) -> PlayerLevel:
    """Return the next level in LEVEL_ORDER, wrapping from EXPERT back to DUMB."""
    idx = LEVEL_ORDER.index(level)
    return LEVEL_ORDER[(idx + 1) % len(LEVEL_ORDER)]


def choose_move(board: Board, colour: Colour, level: PlayerLevel) -> Square:
    """Return a move for *colour* at *level* on *board*.

    Raises ValueError if there are no legal moves.
    """
    config = LEVEL_CONFIGS[level]

    if level == PlayerLevel.DUMB:
        moves = legal_moves(board, colour)
        if not moves:
            raise ValueError(f"No legal moves for {colour}")
        return random.choice(moves)

    if config.use_alpha_beta:
        return best_move_alpha_beta(board, colour, config.depth, scorer=config.scorer)

    return best_move(board, colour, config.depth, scorer=config.scorer)
