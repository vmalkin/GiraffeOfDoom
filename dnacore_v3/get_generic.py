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
    each states fails to the error stae or falls thru to the next one
    initialise
    get data
    parse into list: posix, data
    get most recent date from DB, discard old data
    append new data to DB
    exit
    """
    def __init__(self):
        """State Class - a series of states for this FSM"""
        self.s_initialise = 1
        self.s_get_data = 1
        self.s_parse_data = 1
        self.s_most_recent_date = 1
        self.s_data_append = 1
        self.s_error = 1
        self.s_exit = 1

        self.mag_data = ""

    def do_initialise(self):
        result = "success"
        return result

    def do_get_data(self):
        result = "fail"
        return result

    def do_parse_data(self):
        pass

    def do_most_recent_date(self):
        pass

    def do_data_append(self):
        pass


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
            if state.do_initialise() == "success":
                machine_state = state.s_get_data
            elif machine_state == "fail":
                machine_state = state.s_error
                logging.error("ERROR: unable to init FSM")
            else:
                machine_state = state.s_error
                logging.error("ERROR: Init process FAILED")

        if machine_state == state.s_get_data:
            result = state.do

        if machine_state == state.s_error:
            logging.error("ERROR: Final error state reached")
            machine_state = state.s_exit

        if counter == 100:
            print("Counter Triggered")
            machine_state = state.s_exit

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
