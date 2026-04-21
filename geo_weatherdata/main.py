import constants as k
import time
import mgr_comport
import os
import mgr_database
import mgr_csvfile
from queue import Queue, Empty
from threading import Thread
import numpy as np


# Set up thread to periodically save circular buffer.
class SavedataThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="save_data_thread")

    def run(self):
        while True:
            # Thread should count down until next buffer save. Report any pertinent buffer stats and DB and save errors.
            # Buffer save should occur every 5 minutes or so.
            for i in range(300, 0, -1):
                time.sleep(1)
                if i % 60 ==0:
                    print(f"Buffer size: {weather_data.qsize()} / {weather_data.maxsize}.")
                    print(f"{i} seconds remaining")

            # Begin timer for elapsed processing time.
            timer_start = time.time()
            # When timer has elapsed, save data since last saved from buffer to DB
            batchdata = []

            # block for first item
            item = weather_data.get()
            batchdata.append(item)
            weather_data.task_done()
            # consume the rest from queue.
            while True:
                try:
                    d = weather_data.get_nowait()
                    batchdata.append(d)
                    weather_data.task_done()
                except Empty:
                    break

            # mgr_database.db_data_add expects an array with each element in the array being:
            # [1737274820, '21.05', '99740.46'] (posixtime, temperature, pressure)
            parseddata = []
            for item in batchdata:
                l = item.split(",")
                if len(l) == 3:
                    d0 = safe_float(l[0])
                    d1 = safe_float(l[1])
                    d2 = safe_float(l[2])
                    d = [d0, d1, d2]
                    parseddata.append(d)
                else:
                    print(f"!!! Data is malformed: {item}. Didn't parse.")

            # Save to database.
            mgr_database.db_data_add(parseddata)
            # Save to gzip CSV file.
            mgr_csvfile.csv_save(parseddata)
            # elapsed time for thread processing.
            timer_stop = time.time()
            print(f"Thread processing: {timer_stop - timer_start} seconds.")


def safe_float(x):
    # Make sure a value is a float. Return a NaN if not.
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan


def directory_try_create(directory):
    if os.path.isdir(directory) is False:
        print(f"Creating directory: {directory}")
        try:
            os.makedirs(directory)
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


def  buffer_create():
    buffer = Queue(maxsize=k.buffer_length)
    return buffer


if __name__ == "__main__":
    # initial setup, create database, save folders.
    for key, value in k.dir_saves.items():
        directory_try_create(value)

    if not os.path.isfile(k.database):
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
    weather_data = buffer_create()

    # Set up thread to periodically save circular buffer.
    save_data = SavedataThread()
    try:
        save_data.start()
        print("*** Started save data thread.")
    except:
        print("!!! Unable to start save data thread")

    # Read sensor data and add to buffer
    # We need an exit that GRACEFULLY flushes the contents of the buffer to the DB.
    while True:
        line = com.data_recieve()
        # 1776586101.8807535, 19.27,98792.61
        current_posixtime = time.time()
        dp = f"{current_posixtime},{line}"
        weather_data.put(dp)
        if weather_data.qsize() >= k.buffer_length:
            print(f"!!! Buffer size: {weather_data.qsize()} / {k.buffer_length}.")
            print("!!! Data thread appears to have crashed. Stopping program")
            break
