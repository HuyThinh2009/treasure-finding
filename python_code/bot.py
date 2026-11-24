from abc import ABC, abstractmethod
from typing import Any, Sequence

from state_const import DIRS, State


class Bot(ABC):
    @abstractmethod
    def build_inputs(self, state: State) -> Sequence[Any]:
        """Transform the raw data into model parameters, one item per direction.

        Must return exactly 4 items, in the order: up, right, down, left.
        """

    @abstractmethod
    def predict(self, inputs: Sequence[Any]) -> Sequence[float]:
        """Apply your model to the 4 items returned by build_inputs().

        Must return exactly 4 scores (higher = better), same order as the inputs.
        """


    @abstractmethod
    def accuracy(self, result, path, all_scores):
        pass


class BasicBot(Bot):
    """Tiny greedy example so the harness runs out of the box. Replace with your own."""

    ARGS = [1, 0.35, 0.1, 0.01, 0.2]
    # weights for [is_wall, dist, free_count, direction_priority, not in prev positions]

    def build_inputs(self, state):
        size = len(state.view)
        view_row, view_column = state.view_position
        inputs = []
        direction_priority = 0
        MAX_PRIORITY = 4
        for direction_row, direction_column in DIRS:
            row, column = view_row + direction_row, view_column + direction_column
            is_wall = (
                0 <= row < size
                and 0 <= column < size
                and state.view[row][column] == "1"
            )
            next_position = [
                state.position[0] + direction_row,
                state.position[1] + direction_column,
            ]
            old_dist = self._calculate_dist(state.position, state.target)
            new_dist = self._calculate_dist(next_position, state.target)
            free_count = self._count_free_spaces(
                state.view, direction_row, direction_column
            )
            direction_priority += 1
            is_in_prev_positions =0
            for i in range(len(state.prev_positions)):
                if tuple(next_position) == state.prev_positions[i]:
                    is_in_prev_positions +=1
                    
            inputs.append(
                [
                    int(is_wall),
                    (old_dist - new_dist) / old_dist if old_dist > new_dist else 0,
                    free_count,
                    (MAX_PRIORITY - direction_priority) / MAX_PRIORITY,
                    (4 - is_in_prev_positions) /4,
                ]
            )
        return inputs

    def _calculate_dist(self, position, target):
        return abs(position[0] - target[0]) + abs(position[1] - target[1])

    def _count_free_spaces(self, view, direction_row, direction_column):
        player_position = self._player_position_in_view(view)
        free_count = 0
        total_space = 0
        for x, row in enumerate(view):
            for y, cell in enumerate(row):
                if (
                    (direction_row < 0 and x >= player_position[0])
                    or (direction_row > 0 and x <= player_position[0])
                    or (direction_column < 0 and y >= player_position[1])
                    or (direction_column > 0 and y <= player_position[1])
                ):
                    continue
                total_space += 1
                if cell == "0":
                    free_count += 1
        return free_count / total_space

    def _player_position_in_view(self, view):
        for x, row in enumerate(view):
            for y, cell in enumerate(row):
                if cell == "P":
                    return [x, y]

        raise ValueError("Cannot find player in view.")

    def _values(self, input):
        return [arg * input[index] for index, arg in enumerate(self.ARGS)]

    def predict(self, inputs):
        results = []
        for input in inputs:
            values = self._values(input)
            result = (1 - values[0]) * (values[1] + values[2] + values[3] + values[4])
            results.append(result)
        return results


    def accuracy(self, result, path, all_scores):
        right_move = []
        for i in range(len(path)):
            if right_move and right_move[0] == (path[i]+2)%4:
                right_move.pop(0)
            else:
                right_move = [path[i]] + right_move
        redundant_move = len(path)-len(right_move)
        total_score = len(result)-0.1*redundant_move
        return total_score