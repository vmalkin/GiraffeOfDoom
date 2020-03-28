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
station_id = "Ruru_Obs"


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
        self.s_get_data = 2
        self.s_parse_data = 3
        self.s_most_recent_date = 4
        self.s_data_append = 5
        self.s_error = 6
        self.s_exit = 7

        self.nowdate = int(time.time())
        self.mag_data = []

    def do_initialise(self):
        """Initialise the FSM. DO if necessary"""
        result = "success"
        return result

    def do_get_data(self):
        """Get data"""
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
                    # print(row)
                    try:
                        posix_dt = self.utc2posix(r[0])
                        value = round(float(r[1]), 3)
                        dp = str(posix_dt) + "," + str(value)
                        self.mag_data.append(dp)
                    except Exception:
                        print("ERROR: unable to parse time")
                        logging.error("ERROR: unable to parse time")
                except IndexError:
                    logging.error("ERROR: list index out of range")
                    result = "fail"
        else:
            logging.error("ERROR: Could not get data from URL")
            result = "fail"

        if len(self.mag_data) > 2:
            result = "success"
        # print(self.mag_data)
        return result

    def do_parse_data(self):
        """Parse the magdata from the most recent date."""
        result = "fail"
        tempdata = []
        for row in self.mag_data:
            row = row.split(",")


        return result

    def do_most_recent_date(self):
        result = "success"
        # select max(posix_time) from station_data where station_data.station_id = "Ruru_Obs" order by posix_time asc;
        # query_result = db.execute("select max(posix_time) from station_data where station_data.station_id = ""Ruru_Obs"" order by posix_time asc")
        query_result = db.execute("select max(posix_time) from station_data order by posix_time asc")
        if query_result.arraysize > 0:
            self.nowdate = query_result.fetchone()
            self.nowdate = self.nowdate[0]
        return result

    def do_data_append(self):
        """Append the magdata to the database."""
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
    # print(machine_state)
    #  This loop needs to run until we reach the exit state.
    while machine_state != state.s_exit:
        counter = counter + 1
        # #######################################
        # test to see if we can change state
        if machine_state == state.s_initialise:
            transition = state.do_initialise()
            if transition == "success":
                machine_state = state.s_get_data
                print("INFO: get data")
                logging.info("INFO: get data")
            elif transition == "fail":
                machine_state = state.s_error
                print("ERROR: unable to get data")
                logging.error("ERROR: unable to get data")
            else:
                machine_state = state.s_error
                print("ERROR: get data process FAILED")
                logging.error("ERROR: get data process FAILED")

        if machine_state == state.s_get_data:
            transition = state.do_get_data()
            if transition == "success":
                machine_state = state.s_most_recent_date
                print("INFO: get most recent date from databse")
                logging.info("INFO: get most recent date from databse")
            elif transition == "fail":
                machine_state = state.s_error
                print("ERROR: unable to get most recent date from DB")
                logging.error("ERROR: unable to get most recent date from DB")
            else:
                machine_state = state.s_error
                print("ERROR: get most recent date FAILED")
                logging.error("ERROR: get most recent date FAILED")

        if machine_state == state.s_most_recent_date:
            transition = state.do_most_recent_date()
            if transition == "success":
                machine_state = state.s_parse_data
                print("INFO: Appending new data to DB")
                logging.info("INFO: Appending new data to DB")
            elif transition == "fail":
                machine_state = state.s_error
                print("ERROR: unable to append data to DB")
                logging.error("ERROR: unable to append data to DB")
            else:
                machine_state = state.s_error
                print("ERROR: append to db FAILED")
                logging.error("ERROR: append to db FAILED")

        if machine_state == state.s_parse_data:
            transition = state.do_parse_data()
            if transition == "success":
                machine_state = state.s_data_append
            if transition == "fail":
                machine_state = state.s_error
                print("ERROR: Unable to parse device data")
                logging.error("ERROR: Unable to parse device data")

        if machine_state == state.s_data_append:
            transition = state.do_data_append()
            if transition == "success":
                machine_state = state.s_exit
                print("INFO: Process finished normally. Exiting.")
                logging.info("INFO: Process finished normally. Exiting.")
            elif transition == "fail":
                machine_state = state.s_error
                print("CRITICAL ERROR: unable to exit FSM")
                logging.critical("CRITICAL ERROR: unable to exit FSM")
            else:
                machine_state = state.s_error
                print("CRITICAL ERROR: Init process FAILED")
                logging.error("CRITICAL ERROR: Init process FAILED")

        if machine_state == state.s_exit:
            break

        if machine_state == state.s_error:
            print("ERROR: Final error state reached")
            logging.error("ERROR: Final error state reached")
            machine_state = state.s_exit

        if counter == 100:
            print("Counter Triggered")
            machine_state = state.s_exit

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
