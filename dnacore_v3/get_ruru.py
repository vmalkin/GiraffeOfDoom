import sqlite3
import constants as k


class State:
    """State Class - a series of states for this FSM"""
    data_append = "data_append"
    data_connect = "data_connect"
    initialise = "initialise"
    exit = "exit"

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
state = State()
machine_state = state.initialise

def exit():
    pass


if __name__ == "__main__":
    while True:
        # perform state action
        if machine_state == state.initialise:
            print(machine_state)

        if machine_state == state.exit:
            print(machine_state)

        # test to see if we can change state
        if machine_state == state.initialise:
            print("init --> Data connect")
            machine_state = state.data_connect

        if machine_state == state.data_connect:
            machine_state = state.exit

        if machine_state == state.exit:
            print(machine_state)
            db.close()
            break

    # dna_core = sqlite3.connect(k.dbfile)
    # db = dna_core.cursor()
    # dna_core.commit()
    # db.close()