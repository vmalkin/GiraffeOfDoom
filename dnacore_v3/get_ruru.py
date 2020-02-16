import sqlite3
import constants as k
import logging

"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.WARNING
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")


class State:
    """State Class - a series of states for this FSM"""
    s_data_append = "data_append"
    s_data_connect = "data_connect"
    s_initialise = "initialise"
    s_error = "error"
    s_exit = "exit"


dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
state = State()

machine_state = state.s_initialise
error_string = ""


def exit_app():
    pass


if __name__ == "__main__":
    while True:
        # #######################################
        # perform state action
        if machine_state == state.s_initialise:
            print(machine_state)

        if machine_state == state.s_exit:
            print(machine_state)

        # #######################################
        # test to see if we can change state
        if machine_state == state.s_initialise:
            print("init --> Data connect")
            machine_state = state.s_data_connect

        if machine_state == state.s_data_connect:
            machine_state = state.s_data_append

        if machine_state == state.s_data_append:
            machine_state = state.s_exit

        if machine_state == state.s_error:
            machine_state == state.s_exit

        if machine_state == state.s_exit:
            print(machine_state)
            break

    dna_core.commit()
    db.close()
