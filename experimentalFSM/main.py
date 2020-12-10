from enum import Enum, auto

class States(Enum):
    s_drive = auto()
    s_left = auto()
    s_right = auto()


robot_state = States.s_left


def test_transition(state):
    """Test to see if the robot can change state, if so, change state"""
    currentstate = state

    return currentstate


def do_action(state):
    """Perform the action for the current state"""
    pass


if __name__ == "__main__":
    robot_state = test_transition(robot_state)
    do_action(robot_state)
