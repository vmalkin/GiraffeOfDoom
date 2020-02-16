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
    s_initialise = "initialise"
    s_data_connect = "data_connect"
    s_data_append = "data_append"
    s_error = "error"
    s_exit = "exit"

    def do_initialise(self):
        pass

    def do_data_connect(self):
        print("Connecting...")
        returnmessage = "success"
        return returnmessage

    def do_data_append(self):
        print("Appending...")
        returnmessage = "success"
        return returnmessage

    def do_error(self, errormessage="error"):
        print("AN error occurred")
        returnmessage = "success"
        try:
            logging.error(errormessage)
        except Exception:
            returnmessage = "success"
        return returnmessage

    def do_exit(self):
        pass


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
        # test to see if we can change state
        if machine_state == state.s_initialise:
            result = state.do_initialise()
            machine_state = state.s_data_connect

        if machine_state == state.s_data_connect:
            result = state.do_data_connect()
            if result == "success":
                machine_state = state.s_data_append
            elif result == "fail":
                machine_state = state.s_error

        if machine_state == state.s_data_append:
            result = state.do_data_append()
            if result == "success":
                machine_state = state.s_exit
            elif result == "fail":
                machine_state = state.s_error

        if machine_state == state.s_error:
            state.do_error()
            machine_state = state.s_exit

        if machine_state == state.s_exit:
            break

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
