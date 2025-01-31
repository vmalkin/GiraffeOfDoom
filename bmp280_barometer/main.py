import math
import constants as k
import mgr_comport
import time
import os
import logging
import re
import standard_stuff
import random
import mgr_matplot
import mgr_database


errorloglevel = logging.ERROR
logging.basicConfig(filename="gnss.log", format='%(asctime)s %(message)s', level=errorloglevel)
random.seed()
# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 25


# *************************************************
# Plotter and query processor thread
# *************************************************
# class QueryProcessor(Thread):
#     def __init__(self):
#         Thread.__init__(self, name="QueryProcessor")
#
#     def run(self):
#         # put query data_s4 processing stuff here.
#         while True:
#             wiggle = random.randint(-180, 180)
#             sleeptime = (60 * 15) + wiggle
#             print('Next plot in ' + str(sleeptime) + ' seconds.')
#             time.sleep(sleeptime)
#
#             print("***************************** Start Query Processor")
#             now = int(time.time())
#             timeinterval = now - (60 * 60 * 24)
#             queryresult = mgr_database.db_get_pressure(timeinterval)
#             savefile = k.dir_images + os.sep + "pressure.png"
#             mgr_matplot.plot_time_data(queryresult, savefile)
#             # savefile = k.dir_images + os.sep + "dxdt.png"
#             # mgr_matplot.plot_time_dxdt(queryresult, savefile)
#
#             print("******************************* End Query Processor")


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


def add_data(collection, current_posixtime, csv_line):
    # Will need to add a try except here. Just return the collection
    # if there's a problem.
    try:
        temp = csv_line[0]
        pressure = csv_line[1]
        dp = [current_posixtime, temp, pressure]
        collection.append(dp)
    except:
        print("Unable to parse data to add to collection")
    return collection


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(k.sat_database) is False:
        print("No database file, initialising")
        mgr_database.db_create()

    if os.path.isfile(k.sat_database) is True:
        print("Database file exists")

    if os.path.isdir(k.dir_images) is False:
        print("Creating image file directory...")
        create_directory(k.dir_images)

    # queryprocessor = QueryProcessor()
    # queryprocessor.start()

    com = mgr_comport.SerialManager(k.comport, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
    collection = []
    while True:
        current_posixtime = get_rounded_posix_()
        line = com.data_recieve()
        csv_line = re.split(r'[,|*]', line)

        collection = add_data(collection, current_posixtime, csv_line)
        # Once our collection of data is large enough, process.
        # This delay reduces the risk of the database being locked for charting

        if len(collection) >= 60 * 5:
            mgr_database.db_data_add(collection)
            collection = []
            now = standard_stuff.posix2utc(current_posixtime, '%Y-%m-%d %H:%M')
            print(now, "Barometer data added.")
        # # ENTER into database
