import constants as k
import mgr_comport
import time
import os
import logging
from threading import Thread
import mgr_database
import mgr_plot

errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

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
            result = mgr_database.qry_get_last_24hrs(start_time, "GPGGA")
            mgr_plot.wrapper(result, "GPS")

            print("******************************* End Query Processor")
            time.sleep((60 * 15))


# def posix2utc(posixtime, timeformat):
#     # print(posixtime)
#     # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
#     utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
#     return utctime
#
# def utc2posix(utcstring, timeformat):
#     utc_time = time.strptime(utcstring, timeformat)
#     epoch_time = timegm(utc_time)
#     return epoch_time


def create_directory(directory):
    try:
        os.makedirs(directory)
        print("Directory created.")
    except:
        if not os.path.isdir(directory):
            print("Unable to create directory")
            logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(k.sat_database) is False:
        print("No database file, initialising")
        mgr_database.database_create()
    if os.path.isfile(k.sat_database) is True:
        print("Database file exists")

    if os.path.isdir(k.dir_logfiles) is False:
        print("Creating log file directory...")
        create_directory(k.dir_logfiles)

    if os.path.isdir(k.dir_images) is False:
        print("Creating image file directory...")
        create_directory(k.dir_images)

    # #################################################################################
    # Start threads to process data
    queryprocessor = QueryProcessor()
    queryprocessor.start()

    com = mgr_comport.SerialManager(k.comport, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

    while True:
        # Get com data
        line = com.data_recieve()
        csv_line = line.split(",")
        # print(len(csv_line))

        if len(csv_line) == 15:
            # if the sentence is a GGA sentence from any constellation
            if csv_line[0] == "$GPGGA" or csv_line[0] == "$GLGGA":
                constellation = csv_line[0][1:]
                lat = csv_line[2]
                long = csv_line[4]
                position_fix = int(csv_line[6])
                num_sats = csv_line[7]
                hdop = csv_line[8]
                alt = csv_line[9]

                # If we have a valid position fix
                if position_fix > 0:
                    posixtime = int(time.time())
                    mgr_database.qry_add_data(constellation, posixtime, lat, long, position_fix, num_sats, hdop, alt)
        else:
            logdata = "ERROR: Malformed NMEA sentence: " + line
            print(logdata)
            logging.error(logdata)

    # #################################################################################
