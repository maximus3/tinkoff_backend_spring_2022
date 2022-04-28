from enum import IntEnum


class Status(IntEnum):
    OK = 0
    ERROR_404 = 1
    ERROR = 2
    PARSE_ERROR = 3
