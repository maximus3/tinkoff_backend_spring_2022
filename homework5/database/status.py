from enum import IntEnum


class Status(IntEnum):
    OK = 0
    MOVIE_NOT_FOUND = 1
    INSTANCE_CREATE_FAILED = 2
    MOVIE_UPDATE_FAILED = 3
    WRONG_RATING = 4
    DB_ERROR = 5


class StatusException(Exception):
    def __init__(self, status: Status) -> None:
        super().__init__()
        self.status = status

    def __str__(self) -> str:
        return str(self.status)
