from enum import Enum


class ProblemStatus(str, Enum):
    OK = 'OK'
    WRONG_ANSWER = 'WA'
    TIME_LIMIT = 'TL'
    RUNTIME_ERROR = 'RE'

    WAITING = 'WAITING'
    TESTING = 'TESTING'
