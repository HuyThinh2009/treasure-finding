from dataclasses import dataclass, field
from typing import List, Tuple

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 0 up, 1 right, 2 down, 3 left
START = (0, 0)  # the player always starts at absolute (0, 0)


# --------------------------------------------------------------------------- #
# What the bot sees
# --------------------------------------------------------------------------- #
@dataclass
class State:
    view: List[List[str]]  # raw view from the sample: "P" player, "1" wall, "0" free
    position: Tuple[int, int]  # current absolute (row, column); starts at (0, 0)
    view_position: Tuple[
        int, int
    ]  # current (row, column) inside `view` (starts at the center)
    target: Tuple[int, int]  # absolute (row, column) of the target
    step: int  # number of moves made so far


# --------------------------------------------------------------------------- #
# Harness
# --------------------------------------------------------------------------- #
@dataclass
class Episode:
    path: List[int]  # moves the bot made inside the view
    final_position: Tuple[int, int]
    stop_reason: str  # "exit_view" | "hit_wall" | "max_steps"
    all_scores: List[List[float]] = field(
        default_factory=list
    )  # scores returned by the bot at each step
