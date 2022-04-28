import random

import utils
from static_data import FieldElems, MoveResult, Direction, ShipsData
from text_data import TextData


class Player:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[FieldElems.EMPTY] * width for _ in range(height)]
        self.enemy_field = [[FieldElems.EMPTY] * width for _ in range(height)]
        self.border = utils.get_border(width)
        self.ships_data = []
        self.coords_to_ships_index = {}
        field_area = height * width
        search_ships_count = 4
        while True:
            if (
                sum(
                    [
                        cur_ships_count
                        * (search_ships_count - cur_ships_count + 1)
                        for cur_ships_count in range(1, search_ships_count + 1)
                    ]
                )
                / field_area
                > 0.25
            ):
                search_ships_count -= 1
                break
            search_ships_count += 1
        self.ships = {
            search_ships_count - cur_ships_count + 1: cur_ships_count
            for cur_ships_count in range(1, search_ships_count + 1)
        }
        self.auto_arrange_ships()
        self.ships_count = len(self.ships_data)

    def _get_available_location(self, size, direction):
        available_locations = []
        for row_index in range(self.height):
            for col_index in range(self.width):
                if direction == Direction.HORIZONTAL:
                    last_element_index = col_index + size
                    if last_element_index > self.width:
                        continue
                    for offset in range(size):
                        if (
                            self.field[row_index][col_index + offset]
                            != FieldElems.EMPTY
                        ):
                            break
                    else:
                        available_locations.append((row_index, col_index))
                else:
                    last_element_index = row_index + size
                    if last_element_index > self.height:
                        continue
                    for offset in range(size):
                        if (
                            self.field[row_index + offset][col_index]
                            != FieldElems.EMPTY
                        ):
                            break
                    else:
                        available_locations.append((row_index, col_index))
        return random.choice(available_locations)

    def auto_arrange_ships(self):
        for size in self.ships:
            for _ in range(self.ships[size]):
                direction = random.choice(
                    [Direction.VERTICAL, Direction.HORIZONTAL]
                )
                row_index, col_index = self._get_available_location(
                    size, direction
                )
                ship = ()
                empty_area = ()
                if direction == Direction.HORIZONTAL:
                    for offset in range(size):
                        self.field[row_index][
                            col_index + offset
                        ] = FieldElems.SHIP
                        ship = ship + ((row_index, col_index + offset),)
                        if row_index > 0:
                            self.field[row_index - 1][
                                col_index + offset
                            ] = FieldElems.NEAR
                            empty_area = empty_area + (
                                (row_index - 1, col_index + offset),
                            )
                        if row_index < self.height - 1:
                            self.field[row_index + 1][
                                col_index + offset
                            ] = FieldElems.NEAR
                            empty_area = empty_area + (
                                (row_index + 1, col_index + offset),
                            )
                    for offset in range(-1, 2, 1):
                        if 0 <= row_index + offset < self.height:
                            if col_index > 0:
                                self.field[row_index + offset][
                                    col_index - 1
                                ] = FieldElems.NEAR
                                empty_area = empty_area + (
                                    (row_index + offset, col_index - 1),
                                )
                            if col_index + size < self.width:
                                self.field[row_index + offset][
                                    col_index + size
                                ] = FieldElems.NEAR
                                empty_area = empty_area + (
                                    (row_index + offset, col_index + size),
                                )
                else:
                    for offset in range(size):
                        self.field[row_index + offset][
                            col_index
                        ] = FieldElems.SHIP
                        ship = ship + ((row_index + offset, col_index),)
                        if col_index > 0:
                            self.field[row_index + offset][
                                col_index - 1
                            ] = FieldElems.NEAR
                            empty_area = empty_area + (
                                (row_index + offset, col_index - 1),
                            )
                        if col_index < self.width - 1:
                            self.field[row_index + offset][
                                col_index + 1
                            ] = FieldElems.NEAR
                            empty_area = empty_area + (
                                (row_index + offset, col_index + 1),
                            )
                    for offset in range(-1, 2, 1):
                        if 0 <= col_index + offset < self.width:
                            if row_index > 0:
                                self.field[row_index - 1][
                                    col_index + offset
                                ] = FieldElems.NEAR
                                empty_area = empty_area + (
                                    (row_index - 1, col_index + offset),
                                )
                            if row_index + size < self.height:
                                self.field[row_index + size][
                                    col_index + offset
                                ] = FieldElems.NEAR
                                empty_area = empty_area + (
                                    (row_index + size, col_index + offset),
                                )
                self.ships_data.append(
                    ShipsData(coords=ship, empty_area=empty_area)
                )
                for coords in ship:
                    self.coords_to_ships_index[coords] = (
                        len(self.ships_data) - 1
                    )
        for row_index in range(self.height):
            for col_index in range(self.width):
                if self.field[row_index][col_index] == FieldElems.NEAR:
                    self.field[row_index][col_index] = FieldElems.EMPTY

    def print_fields(self):
        print(self.border + "\t" + self.border)
        for row_num in range(len(self.field)):
            num = f"{row_num + 1:2}"
            print(num, *self.field[row_num], num, sep="", end="\t")
            print(num, *self.enemy_field[row_num], num, sep="")
        print(self.border + "\t" + self.border)

    def make_move(self, row_index, col_index, enemy):
        if (
            row_index < 0
            or col_index < 0
            or row_index >= self.height
            or col_index >= self.width
        ):
            return False, TextData.ERROR_INDEX_OUT_OF_RANGE
        if (
            enemy.field[row_index][col_index] == FieldElems.FIRE
            or enemy.field[row_index][col_index] == FieldElems.MISS
        ):
            return (
                False,
                TextData.WRONG_ELEM + enemy.field[row_index][col_index],
            )
        if enemy.field[row_index][col_index] == FieldElems.EMPTY:
            enemy.field[row_index][col_index] = FieldElems.MISS
            self.enemy_field[row_index][col_index] = FieldElems.MISS
            return True, MoveResult.EMPTY
        if enemy.field[row_index][col_index] == FieldElems.SHIP:
            enemy.field[row_index][col_index] = FieldElems.FIRE
            self.enemy_field[row_index][col_index] = FieldElems.FIRE
            if enemy.ship_is_sink(row_index, col_index):
                enemy.ships_count -= 1
                self.fill_after_sink(row_index, col_index, enemy)
                if enemy.ships_count == 0:
                    return True, MoveResult.WIN
                return True, MoveResult.SINK
            return True, MoveResult.HIT
        print(row_index, col_index, enemy.field[row_index][col_index])
        raise RuntimeError()

    def ship_is_sink(self, row_index, col_index):
        ship_data = self.ships_data[
            self.coords_to_ships_index[(row_index, col_index)]
        ]
        ship_data.not_hit -= 1
        if ship_data.not_hit == 0:
            return True
        return False

    def fill_after_sink(self, row_index, col_index, enemy):
        ship_data = enemy.ships_data[
            enemy.coords_to_ships_index[(row_index, col_index)]
        ]
        for coords in ship_data.empty_area:
            enemy.field[coords[0]][coords[1]] = FieldElems.MISS
            self.enemy_field[coords[0]][coords[1]] = FieldElems.MISS

    def get_len_of_field(self):
        return len(self.border)
