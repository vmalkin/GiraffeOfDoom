import constants as k
from time import time
import mgr_comport
from os import path, makedirs
import mgr_database
from collections import deque

buffer_length = (24 * 60 * 60 * k.sensor_reading_frequency) + 100

def add_data(collection, current_posixtime, csv_line):
    # Will need to add a try except here. Just return the collection
    # if there's a problem.
    try:
        seismodata = csv_line[0]
        temperature = csv_line[1]
        pressure = csv_line[2]
        # Test for seismic data, temp and pressure as floats, otherwise do not use this data.
        if test_isnumber(temperature):
            if test_isnumber(pressure):
                dp = [current_posixtime, seismodata, temperature, pressure]
                collection.append(dp)
    except:
        print(f"Unable to parse data to add to collection: {csv_line}")
    return collection


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


def try_create_directory(directory):
    if path.isdir(directory) is False:
        print(f"Creating directory: {directory}")
        try:
            makedirs(directory)
        except:
            if not path.isdir(directory):
                print("Unable to create directory")


if __name__ == "__main__":
    # initial setup, create database, save folders.
    for key, value in k.dir_saves.items():
        try_create_directory(value)

    if not path.isfile(k.database):
        print("No database file, initialising")
        mgr_database.db_create()

    # Set up the com port.
    com = mgr_comport.SerialManager(k.comport,
                                    k.baudrate,
                                    k.bytesize,
                                    k.parity,
                                    k.stopbits,
                                    k.timeout,
                                    k.xonxoff,
                                    k.rtscts,
                                    k.writeTimeout,
                                    k.dsrdtr,
                                    k.interCharTimeout)

    # Prepopulate circular buffer with saved data if applicable

    # Set up thread to periodically save circular buffer.
    # Thread should count down until next buffer save. Report any pertinant buffer stats and DB and save errors.
    # Buffer save should occur every 5 minutes or so.
    # In thread:
    # When timer has elapsed, save data since last savedate from buffer to DB, then save the current dates data from
    # the database to logfile. IF the clock has ticked over to a new day, do one last save of previous days data, as
    # well as a save of new days data to new file.
    # Files can be GZIPPED automatically

    # Set up thread to periodically create plot of the last day.

    # Read sensor data and add to circular buffer
    while True:
        line = com.data_recieve()
        # 1776586101.8807535, 19.27,98792.61
        current_posixtime = time()
        print(f"{current_posixtime}, {line}")