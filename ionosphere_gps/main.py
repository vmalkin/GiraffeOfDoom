import re
import constants as k
import mgr_comport
import time
import os
import sqlite3
import datetime
import logging
from statistics import mean, stdev
from threading import Thread
import mgr_database
import mgr_plot
import mgr_heatmaps
import numpy as np
from calendar import timegm

errorloglevel = logging.CRITICAL
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

            print("******************************* End Query Processor")
            time.sleep((60 * 15))
            # time.sleep(60)


def nmea_sentence(sentence):
    s = sentence[1:]
    s = s.split("*")
    s = s[0].split(",")
    return s


def sanitise_data(item):
    # Turn a data into a float
    i = 0
    regex = "\d{1,3}[^a-z]"
    if len(item) > 0:
        if len(item) <= 3:
            if re.match(regex, item):
                i = float(item)
    return i


def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


def create_directory(dir):
    try:
        os.makedirs(dir)
        print("Directory created.")
    except:
        if not os.path.isdir(dir):
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


    oldtimer = time.time()
    while True:
        # Get com data
        line = com.data_recieve()
        print(line)
        # if line[:6] == "$GPGSV":
        #     # if line[:6] == "$GPGSV" or line[:6] == "$GLGSV":
        #     sentence = nmea_sentence(line)
        #     # make sure GSV sentence is a multiple of 4

        oldtimer = time.time()
    # #################################################################################

