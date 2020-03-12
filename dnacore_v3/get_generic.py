import sqlite3
import constants as k
import logging
import requests

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

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
datasource = "http://www.ruruobservatory.org.nz/dr01_1hr.csv"


class State:
    """
    Define states.
    have a do_method() for each state. The do_method returns success or fail.
    """
    def __init__(self):
        """State Class - a series of states for this FSM"""
        self.s_initialise = "initialise"
        self.s_data_connect = "data_connect"
        self.s_data_get = "data_get"
        self.s_get_date = "get_date"
        self.s_parse_data = "parse_data"
        self.s_data_append = "data_append"
        self.s_error = "error"
        self.s_exit = "exit"
        self.mag_data = ""

    def do_initialise(self):
        result = "success"
        return result

    def do_data_connect(self):
        result = "success"
        return result

    def do_data_get(self):
        result = "success"
        return result

    def do_get_date(self):
        result = "success"
        return result

    def do_parse_data(self):
        result = "success"
        return result

    def do_data_append(self):
        result = "success"
        return result

    def do_error(self):
        result = "success"
        return result

    def do_exit(self):
        result = "success"
        print("Exiting FSM")
        return result

state = State()
machine_state = state.s_initialise

if __name__ == "__main__":
    counter = 0
    #  This loop needs to run until we reach the exit state.
    while machine_state != state.s_exit:
        counter = counter + 1
        # #######################################
        # test to see if we can change state
        if machine_state == state.s_initialise:
            result = state.do_initialise()
            machine_state = state.s_data_connect

        if counter == 100:
            machine_state = state.s_exit

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
