from collections import namedtuple
from enum import Enum


SIZE_LIMIT = 10
AUTOSAVE_NAME = "autosave.pkl"


class MoveResult(Enum):
    WIN = 1
    SINK = 2
    HIT = 3
    EMPTY = 4


class ProcessInputResult(Enum):
    OK = 1
    SAVE = 2
    WRONG = 3


class Direction(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


FieldElems = namedtuple(
    "FieldElems", ["EMPTY", "SHIP", "NEAR", "FIRE", "MISS"]
)(" . ", " 0 ", "", " * ", " E ")


class ShipsData:
    def __init__(self, coords, empty_area):
        self.coords = coords
        self.empty_area = empty_area
        self.not_hit = len(coords)
