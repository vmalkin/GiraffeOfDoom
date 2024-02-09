import math
import constants as k
import mgr_comport
import time
import os
import logging
from threading import Thread
import re
import standard_stuff
from datetime import datetime
from calendar import timegm
import mgr_database


errorloglevel = logging.ERROR
logging.basicConfig(filename="gnss.log", format='%(asctime)s %(message)s', level=errorloglevel)

# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 25


# *************************************************
# Plotter and query processor thread
# *************************************************
class QueryProcessor(Thread):
    def __init__(self):
        Thread.__init__(self, name="QueryProcessor")

    def run(self):
        # put query data_s4 processing stuff here.
        while True:
            print("***************************** Start Query Processor")
            start_time = int(time.time() - (3 * 24 * 60 * 60))

            # Get data for each constellation.
            # result = mgr_database.qry_get_last_24hrs(start_time, "GPGGA")
            # mgr_plot.wrapper(result, "GPS")

            print("******************************* End Query Processor")
            time.sleep((1800))


def get_rounded_posix_():
    t = time.time()
    t = math.floor(t)
    return t


def create_directory(directory):
    try:
        os.makedirs(directory)
        print("Directory created.")
    except:
        if not os.path.isdir(directory):
            print("Unable to create directory")
            logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")


def parse_msg_id(msgid):
    # print(msgid)
    id_ok = False
    valid_id = ['$GPGSV', '$GPGGA']
    # valid_id = ['$GPGSV', '$GPGGA', '$GPRMC']
    for item in valid_id:
        if msgid == item:
            id_ok = True
    return id_ok


def process_gsv(csv_line):
    pass


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(k.sat_database) is False:
        print("No database file, initialising")
        mgr_database.database_create()

        # init with default values in tables.
        mgr_database.database_initialise()

    if os.path.isfile(k.sat_database) is True:
        print("Database file exists")

    # if os.path.isdir(k.dir_logfiles) is False:
    #     print("Creating log file directory...")
    #     create_directory(k.dir_logfiles)

    if os.path.isdir(k.dir_images) is False:
        print("Creating image file directory...")
        create_directory(k.dir_images)

    # queryprocessor = QueryProcessor()
    # queryprocessor.start()


    com = mgr_comport.SerialManager(k.portName, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

    while True:
        current_posixtime = get_rounded_posix_()
        # Get com data
        # ['$GPGSV', '3', '1', '12', '05', '16', '108', '31', '10', '29', '278', '17', '13', '29', '132', '39', '15', '58', '110', '32', '7B']
        # ['$GPRMC', '002841.00', 'A', '4551.95891', 'S', '17031.19120', 'E', '0.091', '', '080224', '', '', 'D', '65']
        #  ['$GPGGA', '002841.00', '4551.95891', 'S', '17031.19120', 'E', '2', '06', '10.32', '23.7', 'M', '1.8', 'M', '', '0000', '72']
        # typical nmea messages
        line = com.data_recieve()
        csv_line = re.split(r'[,|*]', line)
        msg_id = csv_line[0]

        comport = com

        if parse_msg_id(msg_id) is True :
            # print(csv_line)
            # if msg_id == '$GPGGA':
            #     pass

            if msg_id == '$GPGSV':
                sat_obsv = process_gsv(csv_line)

        # ENTER into database
