import math
import constants as k
import mgr_comport
import time
import os
import re
import mgr_database
import standard_stuff


def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


def get_rounded_posix_():
    t = time.time()
    t = math.floor(t)
    return t


def get_decimal_posix_():
    t = time.time()
    return t


def test_isnumber(numbertotest):
    # Data is ONLY ever a float
    if isinstance(numbertotest, float):
        return True
    # If it's a float cast as a string
    if isinstance(numbertotest, str):
        try:
            float(numbertotest)
            return True
        except ValueError:
            return False
    return False


def add_data(collection, current_posixtime, csv_line):
    # Will need to add a try except here. Just return the collection
    # if there's a problem.
    try:
        seismodata = csv_line[0]
        temperature = csv_line[1]
        pressure = csv_line[2]
        # Test for seismic data, temp and pressure as floats, otherwise do not use this data.
        if test_isnumber(seismodata):
            if test_isnumber(temperature):
                if test_isnumber(pressure):
                    dp = [current_posixtime, seismodata, temperature, pressure]
                    collection.append(dp)
    except:
        print(f"Unable to parse data to add to collection: {csv_line}")
    return collection


if __name__ == "__main__":
    # initial setup, create database, save folders.
    for key, value in k.dir_saves.items():
        try_create_directory(value)

    if not os.path.isfile(k.sat_database):
        print("No database file, initialising")
        mgr_database.db_create()

    if os.path.isfile(k.sat_database):
        print("Database file exists")

    com = mgr_comport.SerialManager(k.comport, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
    collection = []
    while True:
        current_posixtime = get_decimal_posix_()
        line = com.data_recieve()
        # print(line)
        csv_line = re.split(r'[,|*]', line)

        # Test data integrity when adding data
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

            # create logfile
            filename = standard_stuff.posix2utc(current_posixtime, '%Y-%m-%d')  + '.csv'
            savefile = k.dir_saves['logs'] + os.sep + filename
            time_start_24hr = time.time() - (60 * 60 * 24)
            result_24hr = mgr_database.db_data_get(time_start_24hr)
            with open(savefile, 'w') as s:
                for line in result_24hr:
                    l = line + '\n'
                    s.write(l)

