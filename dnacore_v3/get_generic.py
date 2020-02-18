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
    def __init__(self):
        """State Class - a series of states for this FSM"""
        self.s_initialise = "initialise"
        self.s_data_connect = "data_connect"
        self.s_data_get = "data_get"
        self.s_data_append = "data_append"
        self.s_error = "error"
        self.s_exit = "exit"

        self.mag_data = ""

    def do_initialise(self):
        pass

    def do_data_connect(self):
        returnmessage = "success"
        return returnmessage

    def do_data_get(self):
        returnmessage = "fail"
        try:
            result = requests.get(datasource)
            result = result.content.decode('utf-8')
            self.mag_data = result.split('\n')
            print(self.mag_data)
            returnmessage = "success"
        except requests.HTTPError:
            logging.error("Unable to connect to URL")
        finally:
            logging.error("Other fatal http error.")
        return returnmessage

    def do_data_append(self):
        # get data, split into time, data
        db_result = db.execute("select * from station_data where station_id = 'Ruru_Obs'")
        for row in db_result:
            print(row)
        # get the most recent datetime from database else append this data in its entirety
        # parse new data since the most recent datetime
        returnmessage = "fail"
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

state = State()
machine_state = state.s_initialise

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
                machine_state = state.s_data_get
            elif result == "fail":
                machine_state = state.s_error

        if machine_state == state.s_data_get:
            result = state.do_data_get()
            if result == "success":
                machine_state = state.s_data_append
            elif result ==  "fail":
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
