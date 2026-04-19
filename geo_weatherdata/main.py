import constants as k
import time
import mgr_comport
import os
from collections import deque

buffer_length = (24 * 60 * 60 * k.sensor_reading_frequency) + 100


def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print(f"Creating directory: {directory}")
        try:
            os.makedirs(directory)
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


if __name__ == "__main__":
    # initial setup, create database, save folders.
    for key, value in k.dir_saves.items():
        try_create_directory(value)

    com = mgr_comport.SerialManager(k.comport, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

    # Prepopulate circular buffer with saved data if applicable

    # Set up thread to periodically dump circular buffer to logfiles.

    # Set up thread to periodically create plot of the last day.

    # Read sensor data and add to circular buffer
    while True:
        line = com.data_recieve()
        current_posixtime = time.time()
        print(f"{current_posixtime}, {line}")