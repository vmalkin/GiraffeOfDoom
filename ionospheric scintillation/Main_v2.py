import constants as k
import mgr_comport
import time
from threading import Thread
import os
import sqlite3
from statistics import mean, stdev
import datetime
import logging
import re

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

com = mgr_comport.SerialManager(k.portName,k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
timeformat = '%Y-%m-%d %H:%M:%S'
sat_database = "gps_satellites.db"

class SatelliteCollator(Thread):
    def __init__(self):
        Thread.__init__(self, name="SatelliteCollator")

    def run(self):
        while True:
            resultlist = parse_database()
            create_csv(resultlist)
            time.sleep(60*5)


class GPSSatellite:
    def __init__(self, sat_name):
        self.name = sat_name
        self.posixtime = ''
        self.alt = []
        self.az = []
        self.intensity = []
        self.min_array_len = 6

    def set_alt(self, value):
        if value == '':
            appendvalue = 0
        else:
            appendvalue = int(value)
        self.alt.append(appendvalue)

    def set_az(self, value):
        if value == '':
            appendvalue = 0
        else:
            appendvalue = int(value)
        self.az.append(appendvalue)

    def set_intensity(self, value):
        if value == '':
            appendvalue = 0
        else:
            appendvalue = self.calc_intensity(value)
        self.intensity.append(appendvalue)

    def return_alt(self):
        returnvalue = 0
        if len(self.alt) > self.min_array_len:
            returnvalue = round(mean(self.alt), 3)
        return returnvalue

    def return_az(self):
        returnvalue = 0
        if len(self.az) > self.min_array_len:
            returnvalue = round(mean(self.az), 3)
        return returnvalue

    def calc_intensity(self, snr):
        snr = int(snr)
        intensity = 0
        if snr != 0:
            intensity = pow(10, (snr/10))
        return intensity

    def s4_index(self):
        returnvalue = 0
        if len(self.intensity) > self.min_array_len:
            try:
                avg_intensity = mean(self.intensity)
                sigma = stdev(self.intensity)
                returnvalue = round((sigma / avg_intensity), 3)
            except Exception:
                logging.debug("Statistics exception")
        return returnvalue

    def reset(self):
        self.posixtime = ''
        self.alt = []
        self.az = []
        self.intensity = []


def create_database():
    print("No database, creating file")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists satdata;')
    db.execute('create table satdata ('
               'sat_id text,'
               'posixtime integer,'
               'alt real,'
               'az real,'
               's4 real'
               ');')
    gpsdb.commit()
    db.close()


def posix2utc(posixtime):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def parse_database():
    starttime = int(time.time()) - 60*60*28
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select sat_id, posixtime, alt, az, s4 from satdata where posixtime > ? and alt > 20',[starttime])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


def nmea_sentence(sentence):
    sentence = sentence[1:]
    sentence = sentence.split("*")
    sentence = sentence[0].split(",")
    return sentence


def create_csv(resultlist):
    try:
        with open('s4.csv', 'w') as f:
            for result in resultlist:
                dp = str(posix2utc(result[1])) + "," + str(result[4])
                f.write(dp + '\n')
        f.close()
        print("CSV file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")


def create_satellite_list(constellationname):
    returnlist = []
    for i in range(0, 101):
        name = constellationname + str(i)
        gps = GPSSatellite(name)
        returnlist.append(gps)
    return returnlist


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(sat_database) is False:
        print("No database file, initialising")
        create_database()
    if os.path.isfile(sat_database) is True:
        print("Database file exists")

    GPGSV = create_satellite_list("gps_")
    GLGSV = create_satellite_list("glonass_")
    GAGSV = create_satellite_list("galileo_")

    # begin graphing thread
    sat_collation = SatelliteCollator()
    try:
        sat_collation.start()
    except:
        print("Unable to start Satellite Collator")

    counter = 0
    regex_expression = "\A$GPGSV"

    # main loop starts here run every second...
    while True:
        counter = counter + 1
        posix_time = int(time.time())

        # Get com data
        line = com.data_recieve()

        # Parse com data for valid data GSV sentence ???GSV,
        if re.match(regex_expression, line) is True:
            # GSV sentence, parse out the satellite data
            # if valid data, sppend to satellite in lists
            # after 60 seconds, get summarised data and S4 values fron satellites and append to database
            # reset satellite lists
        # end loop
