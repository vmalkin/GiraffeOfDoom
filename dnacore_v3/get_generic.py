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
        self.s_get_date = "get_date"
        self.s_convert_data = "convert_data"
        self.s_parse_data = "parse_data"
        self.s_data_append = "data_append"
        self.s_error = "error"
        self.s_exit = "exit"
        self.mag_data = ""

    def do_initialise(self):
        result = "success"
        return result

    def do_get_date(self):
        result = "fail"
        return result

    def do_convert_data(self):
        result = "success"
        return result

    def do_parse_data(self):
        result = "success"
        return result

    def do_data_append(self):
        result = "success"
        return result

    def do_error(self, error_statement):
        logging.error(error_statement)
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
            machine_state = state.s_get_date

        if machine_state == state.s_get_date:
            result = state.do_get_date()
            if result == "success":
                machine_state = state.do_parse_data()
            elif result == "fail":
                machine_state = state.s_error
                print("ERROR: unable to get data")
                state.do_error("ERROR: unable to get data")
            else:
                machine_state = state.s_error
                print("ERROR: Serious failure of data get")
                state.do_error("ERROR: Serious failure of data get")


        if machine_state == state.s_get_date:
            pass

        if machine_state == state.s_parse_data:
            pass

        if machine_state == state.s_data_append:
            pass

        if machine_state == state.s_error:
            machine_state = state.s_exit

        if counter == 100:
            print("Counter Triggered")
            machine_state = state.s_exit

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
