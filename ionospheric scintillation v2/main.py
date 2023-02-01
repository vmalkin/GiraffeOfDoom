import re

import constants as k
import mgr_comport
import time
import os
import sqlite3
import datetime
import logging
# import re
from statistics import mean, stdev, median
from threading import Thread

import mgr_s4_tracker_v1
import mgr_polar_s4_noise
import mgr_polar_noise_tracks
import mgr_s4_count


errorloglevel = logging.CRITICAL
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

# com = mgr_comport.SerialManager(k.portName, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
#
integration_time = 30
duration = 60*60*24
nullvalue = ""
s4_interval = 24 * 10

# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 25

# This is the query output that will be used to generate graphs and plots etc.
querydata_24 = []
# querydata_48 = []
current_stats = []


def nmea_sentence(sentence):
    s = sentence[1:]
    s = s.split("*")
    s = s[0].split(",")
    return s


def sanitise_data(item):
    # Turn a data into a float
    i = 0
    regex = "\d\d"
    if len(item) == 2:
        if re.match(regex, item):
            i = float(item)
    return i


def satlist_input(sentence, satellite_list):
    # The first four items of the list are messagetype, No of messages, message No, visible satellites
    # Then it's satelliteID, alt, az, SNR, repeating in fours.
    increment = 4
    for i in range(4, len(sentence) - 3, increment):
        sat_index = int(sentence[i])
        sat_alt = sentence[i + 1]
        sat_az = sentence[i + 2]
        sat_snr = sentence[i + 3]

        # if the values are not empty...
        satellite_list[sat_index].alt.append(sanitise_data(sat_alt))
        satellite_list[sat_index].az.append(sanitise_data(sat_az))
        satellite_list[sat_index].snr.append(sanitise_data(sat_snr))

        satellite_list[sat_index].processflag = True
    return satellite_list



# *************************************************
# Plotter and query processor thread
# *************************************************
class QueryProcessor(Thread):
    def __init__(self):
        Thread.__init__(self, name="QueryProcessor")

    def run(self):
        # put query data_s4 processing stuff here.
        # The data recorded consist of:
        # sat_id, posixtime, alt, az, s4, snr
        # for each satellite per minute

        while True:
            print("***************************** Start Query Processor")

            try:
                mgr_s4_tracker_v1.wrapper(s4_interval)
            except:
                print("\n" + "mgr_s4_tracker_v1.wrapper" + "\n")
                logging.warning("mgr_s4_tracker_v1.wrapper failed in MAIN.PY")

            try:
                mgr_polar_s4_noise.wrapper(querydata_24)
            except:
                print("\n" + "mgr_polar_s4_noise.wrapper" + "\n")
                logging.warning("mgr_polar_s4_noise.wrapper failed in MAIN.PY")

            try:
                mgr_polar_noise_tracks.wrapper(querydata_24)
            except:
                print("\n" + "mgr_polar_noise_tracks.wrapper" + "\n")
                logging.warning("mgr_polar_noise_tracks.wrapper failed in MAIN.PY")

            try:
                mgr_s4_count.wrapper()
            except:
                print("\n" + "mgr_s4_count.wrapper" + "\n")
                logging.warning("mgr_s4_count.wrapper failed in MAIN.PY")

            print("\a")
            print("******************************* End Query Processor")
            time.sleep(300)
            # time.sleep(60)


class Satellite:
    def __init__(self, id):
        self.processflag = False
        self.id = id
        self.alt = []
        self.az = []
        self.snr = []


    def calc_intensity(self, snr_array):
        returnarray = []
        for item in snr_array:
            intensity = pow(10, (item / 10))
            returnarray.append(intensity)
        return returnarray

    def get_s4(self):
        # http://mtc-m21b.sid.inpe.br/col/sid.inpe.br/mtc-m21b/2017/08.25.17.52/doc/poster_ionik%20%5BSomente%20leitura%5D.pdf
        if len(self.snr) > 2:
            intensity = self.calc_intensity(self.snr)
            avg_intensity = mean(intensity)
            sigma = stdev(intensity)
            returnvalue = round(((sigma / avg_intensity) * 100), 5)
        else:
            returnvalue = 0
        return returnvalue

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




def database_create():
    print("No database, creating file")
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists satdata;')
    db.execute('create table satdata ('
               'comport_id text,'
               'sat_id text,'
               'posixtime integer,'
               'alt real,'
               'az real,'
               's4 real,'
               'snr real'
               ');')
    gpsdb.commit()
    db.close()


def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def database_parse(hourduration):
    starttime = int(time.time()) - (60 * 60 * hourduration)
    print("Parsing database...")
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()

    result = db.execute('select comport_id, sat_id, posixtime, alt, az, s4, snr from satdata where posixtime > ? and alt > ? order by posixtime asc', [starttime, optimum_altitude])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


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
        database_create()
    if os.path.isfile(k.sat_database) is True:
        print("Database file exists")

    if os.path.isdir(k.dir_logfiles) is False:
        print("Creating log file directory...")
        create_directory(k.dir_logfiles)

    if os.path.isdir(k.dir_images) is False:
        print("Creating image file directory...")
        create_directory(k.dir_images)

    # #################################################################################
    # Start threads to read comports and process data
    queryprocessor = QueryProcessor()

    com = mgr_comport.SerialManager(k.port1, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

    # Set up the lists required to average the satellite values so the DB
    # will store one minute values.
    gpgsv = []
    for i in range(0, 110):
        name = "gps_" + str(i)
        s = Satellite(name)
        gpgsv.append(s)

    glgsv = []
    for i in range(0, 110):
        name = "glo_" + str(i)
        s = Satellite(name)
        glgsv.append(s)

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
            posixtime = int(time.time())
            for s in gpgsv:
                if s.processflag is True:
                    if len(s.snr) > 2:
                        counter = counter + 1
                        gpsdb = sqlite3.connect(k.sat_database)
                        db = gpsdb.cursor()
                        db.execute(
                            'insert into satdata (comport_id, sat_id, posixtime, alt, az, s4, snr) values (?, ?, ?, ?, ?, ?, ?);',
                            [k.comportname, s.id, posixtime, s.get_alt_avg(), s.get_az_avg(), s.get_s4(),
                             s.get_snr_avg()])
                        gpsdb.commit()
                        db.close()
            print(k.comportname, counter, "records added")

            gpgsv = []
            for i in range(0, 110):
                name = "gps_" + str(i)
                s = Satellite(name)
                gpgsv.append(s)

            glgsv = []
            for i in range(0, 110):
                name = "rus_" + str(i)
                s = Satellite(name)
                glgsv.append(s)

            oldtimer = time.time()
            print("Satellite Lists RESET!")

    # queryprocessor.start()
    # #################################################################################

