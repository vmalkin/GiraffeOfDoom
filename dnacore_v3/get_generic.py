import sqlite3
import constants as k
import logging
import requests
import time
import datetime

"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.INFO
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

        self.mag_data = []

    def do_initialise(self):
        result = "success"
        return result

    def do_get_data(self):
        result = "fail"
        try:
            webdata = requests.get(datasource, timeout=20)
        except Exception:
            logging.error("Unable to get data from URL")

        if webdata.status_code == 200:
            # else parse for datetime, data
            webdata = webdata.content.decode('utf-8')
            webdata = webdata.split('\n')

            # the first line is just header data
            webdata.pop(0)

            # convert datetime to posix values
            for row in webdata:
                try:
                    r = row.split(',')
                    print(row)
                    posix_dt = self.utc2posix(r[0])
                    value = round(float(r[1]), 3)
                    dp = str(posix_dt) + "," + str(value)
                    self.mag_data.append(dp)
                    result = "success"
                except IndexError:
                    logging.error("ERROR: list index out of range")
                    result = "fail"
        else:
            logging.error("ERROR: Could not get data from URL")
            result = "fail"
        return result

    def do_parse_data(self):
        result = "fail"
        return result

    def do_most_recent_date(self):
        result = "fail"
        return result

    def do_data_append(self):
        result = "fail"
        return result

    def posix2utc(self, posixvalue):
        # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        return utctime

    def utc2posix(self, utc_string):
        dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S').utctimetuple()
        return(int(time.mktime(dt)))


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
            transition = state.do_initialise()
            if transition == "success":
                machine_state = state.s_get_data
                logging.info("INFO: get data")
            elif transition == "fail":
                machine_state = state.s_error
                logging.error("ERROR: unable to get data")
            else:
                machine_state = state.s_error
                logging.error("ERROR: get data process FAILED")

        if machine_state == state.s_get_data:
            transition = state.do_get_data()
            if transition == "success":
                machine_state = state.s_most_recent_date
                logging.info("INFO: get most recent date from databse")
            elif transition == "fail":
                machine_state = state.s_error
                logging.error("ERROR: unable to get most recent date from DB")
            else:
                machine_state = state.s_error
                logging.error("ERROR: get most recent date FAILED")

        if machine_state == state.s_most_recent_date:
            transition = state.do_most_recent_date()
            if transition == "success":
                machine_state = state.s_data_append
                logging.info("INFO: Appending new data to DB")
            elif transition == "fail":
                machine_state = state.s_error
                logging.error("ERROR: unable to append data to DB")
            else:
                machine_state = state.s_error
                logging.error("ERROR: append to db FAILED")


        if machine_state == state.s_data_append:
            transition = state.do_data_append()
            if transition == "success":
                machine_state = state.s_exit
                logging.info("INFO: Process finished normally. Exiting.")
            elif transition == "fail":
                machine_state = state.s_error
                logging.critical("CRITICAL ERROR: unable to exit FSM")
            else:
                machine_state = state.s_error
                logging.error("CRITICAL ERROR: Init process FAILED")

        if machine_state == state.s_exit:
            break

        if machine_state == state.s_error:
            logging.error("ERROR: Final error state reached")
            machine_state = state.s_exit

        if counter == 100:
            print("Counter Triggered")
            machine_state = state.s_exit

    print("Closing database and exiting")
    dna_core.commit()
    db.close()