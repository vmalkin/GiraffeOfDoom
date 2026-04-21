import constants as k
from time import time, sleep
import mgr_comport
from os import path, makedirs
import mgr_database
from collections import deque
from threading import Thread


# Set up thread to periodically save circular buffer.
class SavedataThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="save_data_thread")

    def run(self):
        while True:
            # Thread should count down until next buffer save. Report any pertinent buffer stats and DB and save errors.
            # Buffer save should occur every 5 minutes or so.
            sleep(60)
            # When timer has elapsed, save data since last saved from buffer to DB, then save the current dates data from
            # the database to logfile. IF the clock has ticked over to a new day, do one last save of previous days data, as
            # well as a save of new days data to new file.
            # Files can be GZIPPED automatically
            try:
                print(f"Circular buffer length: {len(weather_data)}")
            except:
                pass


# def data_add(collection, current_posixtime, csv_line):
#     # Will need to add a try except here. Just return the collection
#     # if there's a problem.
#     try:
#         seismodata = csv_line[0]
#         temperature = csv_line[1]
#         pressure = csv_line[2]
#         # Test for temp and pressure as floats, otherwise do not use this data.
#         if number_test(temperature):
#             if number_test(pressure):
#                 dp = [current_posixtime, seismodata, temperature, pressure]
#                 collection.append(dp)
#     except:
#         print(f"Unable to parse data to add to collection: {csv_line}")
#     return collection


def number_test(numbertotest):
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


def directory_try_create(directory):
    if path.isdir(directory) is False:
        print(f"Creating directory: {directory}")
        try:
            makedirs(directory)
        except:
            if not path.isdir(directory):
                print("Unable to create directory")


def  circular_buffer_create():
    buffer = deque(maxlen=k.buffer_length)
    return buffer

if __name__ == "__main__":
    # initial setup, create database, save folders.
    for key, value in k.dir_saves.items():
        directory_try_create(value)

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
    weather_data = circular_buffer_create()

    # Set up thread to periodically save circular buffer.
    save_data = SavedataThread()
    try:
        save_data.start()
        print(f"*** Started save data thread.")
    except:
        print("!!! Unable to start save data thread")

    # Read sensor data and add to circular buffer
    # We need an exit that GRACEFULLY flushes the contents of the buffer to the DB.
    while True:
        line = com.data_recieve()
        # 1776586101.8807535, 19.27,98792.61
        current_posixtime = time()
        dp = f"{current_posixtime},{line}\n"
        weather_data.append(dp)