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
datasource = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-6-hour.json"
station_id = "GOES_16"
timeformat = '%Y-%m-%dT%H:%M:%SZ'

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
                        print("WARNING: unable to parse time")
                        logging.warning("WARNING: unable to parse a time value: " + str(posix_dt))
                except IndexError:
                    logging.warning("WARNING: list index out of range")
                    result = "fail"
        else:
            logging.error("ERROR: Could not get data from URL")
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
            print("ERROR: Error with query")
            logging.error("ERROR: Error with query")
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
                print("INFO: Retrieved most recent date from database")
                logging.info("INFO: Retrieved most recent date from database")
            elif transition == "fail":
                machine_state = state.s_error
                print("ERROR: Failed to retrieve most recent date from database")
                logging.error("ERROR: Failed to retrieve most recent date from database")
            else:
                machine_state = state.s_error
                print("ERROR: Failed to retrieve most recent date from database")
                logging.error("ERROR: Failed to retrieve most recent date from database")

        if machine_state == state.s_parse_data:
            transition = state.do_parse_data()
            if transition == "success":
                machine_state = state.s_data_append
            elif transition == "fail":
                machine_state = state.s_error
                print("ERROR: Unable to parse device data")
                logging.error("ERROR: Unable to parse device data")
            else:
                machine_state = state.s_error
                print("ERROR: Unable to parse device data")
                logging.error("ERROR: Unable to parse device data")

        if machine_state == state.s_data_append:
            transition = state.do_data_append()
            if transition == "success":
                machine_state = state.s_exit
                print("INFO: Data appended to DB.")
                logging.info("INFO: Data appended to DB.")
            elif transition == "fail":
                machine_state = state.s_error
                print("CRITICAL ERROR: Unable to add data to DB")
                logging.critical("CRITICAL ERROR: Unable to add data to DB")
            else:
                machine_state = state.s_error
                print("CRITICAL ERROR: Final Exception - Unable to add data to DB")
                logging.error("CRITICAL ERROR: Final Exception - Unable to add data to DB")

        if machine_state == state.s_exit:
            print("Exiting...")
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
