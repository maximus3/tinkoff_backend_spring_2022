from string import ascii_uppercase
import pickle

from static_data import SIZE_LIMIT, ProcessInputResult, AUTOSAVE_NAME
from text_data import TextData


def get_border(width):
    return "+-" + "".join([f"-{c}-" for c in ascii_uppercase[:width]]) + "-+"


def move_to_str(row_index, col_index):
    return f"{ascii_uppercase[col_index]}{row_index + 1}"


def check_size_limits(height, width):
    if height < SIZE_LIMIT or width < SIZE_LIMIT:
        return (
            False,
            TextData.FIELD_SMALL,
        )
    if width > len(ascii_uppercase):
        return (
            False,
            TextData.FIELD_BIG,
        )
    return True, None


def load_game():
    player, enemy_player = None, None
    try:
        with open(AUTOSAVE_NAME, "rb") as f:
            player, enemy_player = pickle.load(f)
    except Exception:
        pass
    return player, enemy_player


def save_game(player, enemy_player):
    with open(AUTOSAVE_NAME, "wb") as f:
        pickle.dump((player, enemy_player), f)
    return True


def process_input(move):
    if move == "SAVE":
        return ProcessInputResult.SAVE, None, None
    move = move.split()
    if len(move) == 1:
        move = move[0]
        move = [move[:1], move[1:]]
    try:
        row_index, col_index = int(move[1]), ascii_uppercase.index(move[0])
    except ValueError:
        return ProcessInputResult.WRONG, None, None
    row_index -= 1
    return ProcessInputResult.OK, row_index, col_index
