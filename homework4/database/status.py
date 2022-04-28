from enum import IntEnum


class Status(IntEnum):
    OK = 0
    EXISTS = 1
    TIME_EXP = 2
    NO_MONEY = 3
    ERROR = 4
    COUNT_IS_ZERO = 5
