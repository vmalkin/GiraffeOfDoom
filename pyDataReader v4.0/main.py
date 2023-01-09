import serial
from time import time, sleep
from datetime import datetime
import logging
import re
import sys
from threading import Thread
import os
import sqlite3

import mgr_create_daily_logfile
import standard_stuff
import mgr_binner
import mgr_detrended_v2

__version__ = "5.0"
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

# should be set for decimal data only
comport_regex = r'^(\d*\W\d*)$'

station_id = "ruru"   # ID of magnetometer station
database = "arraysave.db"
logfile_dir = "dailylogs"
publish_dir = "publish"

# Comm port parameters - uncomment and change one of the portNames depending on your OS
# portName = 'Com42'  # Windows
# portName = '/dev/tty.usbserial-A9MO3C9T' #MacOS
portName = '/dev/ttyUSB0'
baudrate = 115200
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 60
xonxoff = False
rtscts = True
writeTimeout = None
dsrdtr = False
interCharTimeout = None


# CHARTING FUNCTION AS A THREAD
class ChartThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="SimpleChartingThread")
        print("Starting thread for charting")

    def run(self):
        while True:
            # Chart data every five minutes
            sleep(300)

            # csv logfile for the last 24 hours
            mgr_create_daily_logfile.wrapper(current_data, logfile_dir)

            # Detrended magnetogram/data
            mgr_detrended_v2.wrapper(current_data, publish_dir)

            # unprocessed magnetogram/data

            # Empirical Mode Decomposition of last 24 hours

            # Brendan Davies Aurora data

class SerialManager:
    def __init__(self, portname, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, writeTimeout, dsrdtr, interCharTimeout):
        self._portname = portname
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self._xonxoff = xonxoff
        self._rtscts = rtscts
        self._writeTimeout = writeTimeout
        self._dsrdtr = dsrdtr
        self._interCharTimeout = interCharTimeout

        try:
            self.com = serial.Serial(self._portname, self._baudrate, self._bytesize, self._parity, self._stopbits, self._timeout, self._xonxoff, self._rtscts, self._writeTimeout, self._dsrdtr, self._interCharTimeout)
        except serial.SerialException:
            print("CRITICAL ERROR: Com port not responding. Please check parameters")
            logging.critical("CRITICAL ERROR: Unable to open com port. Please check com port parameters and/or hardware!!")
            print("\n\n" + str(sys.exc_info()))

    def data_recieve(self):
        logdata = self.com.readline()  # logData is a byte array, not a string at this point
        logdata = str(logdata, 'ascii').strip()  # convert the byte array to string. strip off unnecessary whitespace
        return logdata


def getposixtime():
    timevalue = int(time())
    return timevalue


def database_create():
    print("No database, creating file")
    gpsdb = sqlite3.connect(database)
    db = gpsdb.cursor()
    db.execute('drop table if exists data;')
    db.execute('create table data ('
               'posixtime text,'
               'datavalue text'
               ');')
    gpsdb.commit()
    db.close()


def database_add_data(timestamp, datavalue):
    db = sqlite3.connect(database)
    cursor = db.cursor()
    cursor.execute("insert into data (posixtime, datavalue) values (?,?);", [timestamp, datavalue])
    db.commit()
    db.close()


def database_get_data():
    tempdata = []
    starttime = getposixtime() - 86400
    db = sqlite3.connect(database)
    try:
        cursor = db.cursor()
        result = cursor.execute("select * from data where data.posixtime > ? order by data.posixtime asc", [starttime])
        for line in result:
            dt = line[0]
            da = line[1]
            d = [dt, da]
            tempdata.append(d)

    except sqlite3.OperationalError:
        print("Database is locked, try again!")
    db.close()
    return tempdata


def create_directory(path):
    try:
        os.makedirs(path)
        print("Directory created: " + path)
    except:
        if not os.path.isdir(path):
            print("Unable to create directory " + path)
            logging.critical("CRITICAL ERROR: Unable to create logs directory")


if __name__ == "__main__":
    print("Pything Data Logger")
    print("(c) Vaughn Malkin, 2015 - 2023")
    print("Version " + __version__)

    # the current 24 hours of data are stored here to be shared with various aux functions for plotting etc.
    current_data = []

    # set up for logging
    comport = SerialManager(portName, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, writeTimeout, dsrdtr, interCharTimeout)

    # Thread code to implement charting in a new thread.
    grapher_thread = ChartThread()
    try:
        grapher_thread.start()
    except:
        print("Unable to start Charting Thread")
        logging.critical("CRITICAL ERROR: Unable to shart Highcharts Thread")
        print(str(sys.exc_info()))

    # Check that we have folders and database in place
    if os.path.isfile(database) is False:
        print("No database file, initialising")
        database_create()
    
    if os.path.isdir(logfile_dir) is False:
        print("Creating log file directory...")
        create_directory(logfile_dir)
        
    if os.path.isdir(publish_dir) is False:
        print("Creating log file directory...")
        create_directory(publish_dir)

    # The plotting begins here
    while True:
        # single data value from com port
        reading = comport.data_recieve()
        if re.match(comport_regex, reading):
            # get the current POSIX time
            current_dt = getposixtime()

            # create the datapoint. Print the values for the user.
            database_add_data(current_dt, reading)
            print(standard_stuff.posix2utc(current_dt, '%Y-%m-%d %H:%M:%S'), reading)

            # populate the current data array to be shared with plotting functions in thread.
            current_data = database_get_data()

        else:
            print("Garbage data from device: " + reading)
            logging.warning("WARNING: Garbage data from device: " + reading)
