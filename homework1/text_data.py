from string import ascii_uppercase

from static_data import SIZE_LIMIT, AUTOSAVE_NAME


class TextData:
    FIELD_SMALL = f"The field sizes is too small. height and width should me >= {SIZE_LIMIT}"
    FIELD_BIG = (
        f"The field size is too big. width should be <= {len(ascii_uppercase)}"
    )
    ERROR_INDEX_OUT_OF_RANGE = "Index out of range"
    WRONG_ELEM = "Elem is "

    WELCOME = "Welcome to Battleship game!"
    INIT = "Initializing game with height = {0}, width = {1}\n"
    FOUND_AUTOSAVE = "You have autosave. Do you want to load it? Yes/no?: "
    ERROR_LOAD_AUTOSAVE = f"Error in load {AUTOSAVE_NAME}"
    ERROR_DELETE_AUTOSAVE = f"Error in delete {AUTOSAVE_NAME}"

    YOUR_FIELD_NAME = "Your field"
    OPP_FIELD_NAME = "Opponent's field"

    ENTER_MOVE = 'Enter your move (e.g. B1) or type "save" to save your game'
    YOUR_MOVE = "Your move will be "
    GAME_SAVED = "Game saved!"
    WRONG_MOVE = "Wrong move!"
    EMPTY_MOVE = "Empty!"
    HIT_MOVE = "Hit!"
    SINK_MOVE = "Ship is sink!"

    YOU_WIN = "You win!!!"
    YOU_LOSE = "You lose!!!"

    ENEMY_MOVE = "\nEnemy shot {0} - {1}"
