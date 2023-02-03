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
import numpy as np

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
            starttime = time.time() - (60 * 60 * 24)
            alt = 40
            result = mgr_database.qry_get_last_24hrs(starttime, alt)
            result = np.array(result)
            mgr_plot.wrapper(result)

            print("******************************* End Query Processor")
            time.sleep((60 * 15))
            # time.sleep(60)


class Satellite:
    def __init__(self, id):
        self.processflag = False
        self.id = id
        self.visible_sats = 0
        self.alt = []
        self.az = []
        self.snr = []


    def calc_intensity(self, snr_array):
        returnarray = []
        for item in snr_array:
            intensity = pow(10, (item / 10))
            returnarray.append(intensity)
        return returnarray

    def get_alt_avg(self):
        x = 0
        if len(self.alt) > 0:
            x = mean(self.alt)
        return x

    def get_az_avg(self):
        x = 0
        if len(self.az) > 0:
            x = mean(self.az)
        return x

    def get_snr_avg(self):
        x = 0
        if len(self.snr) > 0:
            x = mean(self.snr)
        return x


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


def satlist_input(sentence, satellite_list):
    # The first four items of the list are messagetype, No of messages, message No, visible satellites
    # Then it's satelliteID, alt, az, SNR, repeating in fours.
    increment = 4
    visible_satellites = sentence[3]
    for i in range(4, len(sentence) - 3, increment):
        sat_index = int(sentence[i])
        sat_alt = sentence[i + 1]
        sat_az = sentence[i + 2]
        sat_snr = sentence[i + 3]

        # if the values are not empty...
        satellite_list[sat_index].visible_sats = visible_satellites
        satellite_list[sat_index].alt.append(sanitise_data(sat_alt))
        satellite_list[sat_index].az.append(sanitise_data(sat_az))
        satellite_list[sat_index].snr.append(sanitise_data(sat_snr))

        satellite_list[sat_index].processflag = True
    return satellite_list


def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def create_directory(dir):
    try:
        os.makedirs(dir)
        print("Directory created.")
    except:
        if not os.path.isdir(dir):
            print("Unable to create directory")
            logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")


def satellite_list_create(constellation):
    l = []
    for i in range(0, 110):
        name = constellation + str(i)
        s = Satellite(name)
        l.append(s)
    return l


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

    com = mgr_comport.SerialManager(k.port1, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

    # Set up the lists required to average the satellite values so the DB
    # will store one minute values.
    gpgsv = satellite_list_create("gps")
    glgsv = satellite_list_create("gls")

    oldtimer = time.time()
    while True:
        # Get com data
        line = com.data_recieve()

        if line[:6] == "$GPGSV":
            # if line[:6] == "$GPGSV" or line[:6] == "$GLGSV":
            sentence = nmea_sentence(line)
            # make sure GSV sentence is a multiple of 4
            if len(sentence) % 4 == 0:
                if sentence[0] == "GPGSV":
                    gpgsv = satlist_input(sentence, gpgsv)
                else:
                    glgsv = satlist_input(sentence, glgsv)

        nowtimer = time.time()
        # at least one minute has elapsed
        if nowtimer >= (oldtimer + 60):
            counter = 0
            posixtime = int(nowtimer)
            for s in gpgsv:
                if s.processflag is True:
                    if len(s.snr) > 2:
                        counter = counter + 1
                        gpsdb = sqlite3.connect(k.sat_database)
                        db = gpsdb.cursor()
                        db.execute(
                            'insert into satdata (comport_id, sat_id, posixtime, visible_sats, alt, az, snr) values (?, ?, ?, ?, ?, ?, ?);',
                            [k.port1, s.id, posixtime, s.visible_sats, s.get_alt_avg(), s.get_az_avg(), s.get_snr_avg()])
                        gpsdb.commit()
                        db.close()
            print(posix2utc(nowtimer, '%Y-%m-%d %H:%M'), k.port1, counter, "records added")

            # reset the satellite lists
            gpgsv = satellite_list_create("gps")
            glgsv = satellite_list_create("gls")
            oldtimer = time.time()
    # queryprocessor.start()
    # #################################################################################

