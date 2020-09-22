import sqlite3
import constants as k
import logging
import requests
import time
import datetime
import re

"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.ERROR
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
datasource = "https://services.swpc.noaa.gov/products/solar-wind/mag-2-hour.json"
station_id = "Geomag_Bz"
timeformat = '%Y-%m-%d %H:%M:%S.%f'

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
        self.s_initialise = "s_initialise"
        self.s_get_data = "s_get_data"
        self.s_parse_data = "s_parse_data"
        self.s_most_recent_date = "s_most_recent_date"
        self.s_data_append = "s_data_append"
        self.s_error = "s_error"
        self.s_exit = "s_exit"

        self.nowdate = 0
        self.mag_data = []

    def do_initialise(self):
        """Initialise the FSM. DO if necessary"""
        result = "success"
        return result

    def do_get_data(self):
        """Get data"""
        result = "fail"
        webdata = requests.get(datasource, timeout=20).json()
        returndata = []
        try:
            json_data = webdata
            for i in range(1, len(json_data)):
                time_tag = self.utc2posix(json_data[i][0])
                bz = json_data[i][3]


                if re.match(r"^[0-9]*[0-9.]*$", bz):
                    pass
                else:
                    speed = ""

                dp = str(time_tag) + "," + str(bz)
                returndata.append(dp)
            self.mag_data = returndata

        except ValueError:
            logging.error("ERROR - instruments.py: no valid JSON data for " + str(self.name))
            print("ERROR: no valid JSON data for " + str(self.name))

        finally:
            logging.error(station_id + " ERROR: Could not get data from URL")
            result = "fail"

        if len(self.mag_data) > 2:
            result = "success"
        # print(self.mag_data)
        return result

    def do_parse_data(self):
        """Parse the magdata from the most recent date. Data should have format of posixtime, datavalue. """
        result = "fail"
        tempdata = []
        for row in self.mag_data:
            row = row.split(",")
            # print(row)
            dt = int(row[0])
            data = row[1]
            if dt > int(self.nowdate):
                dp = str(dt) + ", " + str(data)
                tempdata.append(dp)
        if len(tempdata) > 0:
            self.mag_data = tempdata
            result = "success"
        print("Number of records to append: " + str(len(tempdata)))
        return result

    def do_most_recent_date(self):
        result = "success"
        # select max(posix_time) from station_data where station_data.station_id = "Ruru_Obs" order by posix_time asc;
        query_result = db.execute("select max(posix_time) from station_data where station_data.station_id = ? order by posix_time asc", [station_id])
        # query_result = db.execute("select max(posix_time) from station_data order by posix_time asc")
        tempdate = query_result.fetchone()
        tempdate = tempdate[0]
        # print(tempdate)
        if tempdate != None:
            self.nowdate = int(tempdate)
        else:
            pass
        print("Most recent date: " + str(self.nowdate))
        return result

    def do_data_append(self):
        """Append the magdata to the database."""
        result = "fail"
        try:
            for item in self.mag_data:
                itemsplit = item.split(",")
                db.execute("insert into station_data(station_id, posix_time, data_value) values (?, ?, ?)", [station_id, itemsplit[0], itemsplit[1]])
            result = "success"
        except sqlite3.ProgrammingError:
            print(station_id + " ERROR: Error with query")
            logging.error(station_id + " ERROR: Error with query")
        return result

    def posix2utc(self, posixvalue):
        # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime(timeformat)
        return utctime

    def utc2posix(self, utc_string):
        dt = datetime.datetime.strptime(utc_string, timeformat).utctimetuple()
        return(int(time.mktime(dt)))


state = State()
machine_state = state.s_initialise

if __name__ == "__main__":
    counter = 0
    #  This loop needs to run until we reach the exit state.
    while machine_state != state.s_exit:
        counter = counter + 1
        print("Machine State: " + machine_state)
        # #######################################
        # test to see if we can change state
        if machine_state == state.s_initialise:
            transition = state.do_initialise()
            if transition == "success":
                machine_state = state.s_get_data
                print(station_id + " INFO: get data")
                logging.info(station_id + " INFO: get data")
            elif transition == "fail":
                machine_state = state.s_error
                print(station_id + " ERROR: unable to get data")
                logging.error(station_id + " ERROR: unable to get data")
            else:
                machine_state = state.s_error
                print(station_id + " ERROR: get data process FAILED")
                logging.error(station_id + " ERROR: get data process FAILED")

        if machine_state == state.s_get_data:
            transition = state.do_get_data()
            if transition == "success":
                machine_state = state.s_most_recent_date
                print(station_id + " INFO: get most recent date from databse")
                logging.info(station_id + " INFO: get most recent date from databse")
            elif transition == "fail":
                machine_state = state.s_error
                print(station_id + " ERROR: unable to get most recent date from DB")
                logging.error(station_id + " ERROR: unable to get most recent date from DB")
            else:
                machine_state = state.s_error
                print(station_id + " ERROR: get most recent date FAILED")
                logging.error(station_id + " ERROR: get most recent date FAILED")

        if machine_state == state.s_most_recent_date:
            transition = state.do_most_recent_date()
            if transition == "success":
                machine_state = state.s_parse_data
                print(station_id + " INFO: Retrieved most recent date from database")
                logging.info(station_id + " INFO: Retrieved most recent date from database")
            elif transition == "fail":
                machine_state = state.s_error
                print(station_id + " ERROR: Failed to retrieve most recent date from database")
                logging.error(station_id + " ERROR: Failed to retrieve most recent date from database")
            else:
                machine_state = state.s_error
                print(station_id + " ERROR: Failed to retrieve most recent date from database")
                logging.error(station_id + " ERROR: Failed to retrieve most recent date from database")

        if machine_state == state.s_parse_data:
            transition = state.do_parse_data()
            if transition == "success":
                machine_state = state.s_data_append
            elif transition == "fail":
                machine_state = state.s_error
                print(station_id + " ERROR: Unable to parse device data")
                logging.error(station_id + " ERROR: Unable to parse device data")
            else:
                machine_state = state.s_error
                print(station_id + " ERROR: Unable to parse device data")
                logging.error(station_id + " ERROR: Unable to parse device data")

        if machine_state == state.s_data_append:
            transition = state.do_data_append()
            if transition == "success":
                machine_state = state.s_exit
                print(station_id + " INFO: Data appended to DB.")
                logging.info(station_id + " INFO: Data appended to DB.")
            elif transition == "fail":
                machine_state = state.s_error
                print(station_id + " CRITICAL ERROR: Unable to add data to DB")
                logging.critical(station_id + " CRITICAL ERROR: Unable to add data to DB")
            else:
                machine_state = state.s_error
                print(station_id + " CRITICAL ERROR: Final Exception - Unable to add data to DB")
                logging.error(station_id + " CRITICAL ERROR: Final Exception - Unable to add data to DB")

        if machine_state == state.s_exit:
            print("Exiting...")
            break

        if machine_state == state.s_error:
            print(station_id + " ERROR: Final error state reached")
            logging.error(station_id + " ERROR: Final error state reached")
            machine_state = state.s_exit

        if counter == 100:
            print(station_id + " Counter Triggered")
            machine_state = state.s_exit

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
