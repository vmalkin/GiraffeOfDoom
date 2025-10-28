from enum import Enum


class State(Enum):
    GET_DATA = 0
    PARSE_DATA = 1
    ADD_DATA = 2
    ERROR = 3
    SETUP = 4

currentstate = State.SETUP


if __name__ == "__main__":


