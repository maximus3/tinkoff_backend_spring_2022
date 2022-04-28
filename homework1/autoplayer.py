import random

from player import Player
from static_data import FieldElems, MoveResult


class AutoPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_hit = None

    def _get_available_move(self):
        available_moves = []
        for row_index in range(self.height):
            for col_index in range(self.width):
                if self.enemy_field[row_index][col_index] == FieldElems.EMPTY:
                    available_moves.append((row_index, col_index))
        return random.choice(available_moves)

    def make_auto_move(self, enemy_player):
        if self.last_hit is None:
            row_index, col_index = self._get_available_move()
            input_ok, move_res = self.make_move(
                row_index, col_index, enemy_player
            )
            if move_res == MoveResult.HIT:
                self.last_hit = (
                    (row_index, col_index),
                    (row_index, col_index),
                )
            return row_index, col_index, move_res

        moves_first = [
            (self.last_hit[0][0], self.last_hit[0][1] - 1),
            (self.last_hit[1][0], self.last_hit[1][1] + 1),
        ]
        moves_second = [
            (self.last_hit[0][0] - 1, self.last_hit[0][1]),
            (self.last_hit[1][0] + 1, self.last_hit[1][1]),
        ]
        moves = moves_first + moves_second
        if self.last_hit[0] != self.last_hit[1]:
            if self.last_hit[0][0] == self.last_hit[1][0]:
                moves = moves_first
            else:
                moves = moves_second
        input_ok = False
        move_res = None
        row_index, col_index = None, None
        while not input_ok:
            try:
                row_index, col_index = moves.pop()
            except IndexError:
                raise RuntimeError()
            input_ok, move_res = self.make_move(
                row_index, col_index, enemy_player
            )

        if move_res == MoveResult.HIT:
            tmp = sorted(
                (self.last_hit[0], self.last_hit[1], (row_index, col_index))
            )
            self.last_hit = (tmp[0], tmp[-1])
        elif move_res == MoveResult.SINK:
            self.last_hit = None
        return row_index, col_index, move_res
