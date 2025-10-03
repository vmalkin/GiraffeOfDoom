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


# errorloglevel = logging.DEBUG
# logging.basicConfig(filename="gnss.log", format='%(asctime)s %(message)s', level=errorloglevel)
random.seed()
# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 25

def get_rounded_posix_():
    t = time.time()
    t = math.floor(t)
    return t

def get_decimal_posix_():
    t = time.time()
    return t

def create_directory(directory):
    try:
        os.makedirs(directory)
        print("Directory created.")
    except:
        if not os.path.isdir(directory):
            print("Unable to create directory")
            # logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")

def test_isnumber(numbertotest):
    # Data is ONLY ever a float
    pass

def add_data(collection, current_posixtime, csv_line):
    # Will need to add a try except here. Just return the collection
    # if there's a problem.
    try:
        seismodata = csv_line[0]
        temperature = csv_line[1]
        pressure = csv_line[2]
        # Test for temp and pressure as floats.
        dp = [current_posixtime, seismodata, temperature, pressure]
        collection.append(dp)
    except:
        print(f"Unable to parse data to add to collection: {csv_line}")
    return collection


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if not os.path.isfile(k.sat_database):
        print("No database file, initialising")
        mgr_database.db_create()

    if os.path.isfile(k.sat_database):
        print("Database file exists")

    if not os.path.isdir(k.dir_images):
        print("Creating image file directory...")
        create_directory(k.dir_images)

    # queryprocessor = QueryProcessor()
    # queryprocessor.start()

    com = mgr_comport.SerialManager(k.comport, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
    collection = []
    while True:
        current_posixtime = get_decimal_posix_()
        line = com.data_recieve()
        # print(line)
        csv_line = re.split(r'[,|*]', line)

        collection = add_data(collection, current_posixtime, csv_line)
        # Once our collection of data is large enough, process.
        # This delay reduces the risk of the database being locked for charting
        # 5 times per second every 2 minutes
        if len(collection) >= 10 * 60 * 2:
            mgr_database.db_data_add(collection)
            # print(collection)
            collection = []
            now = standard_stuff.posix2utc(current_posixtime, '%Y-%m-%d %H:%M')
            print(f"{now}: Seismograph data added.")
        # # ENTER into database
