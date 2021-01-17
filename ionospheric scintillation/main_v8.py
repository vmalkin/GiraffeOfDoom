import constants as k
import mgr_comport
import time
import os
import sqlite3
import datetime
import logging
import re
from statistics import mean, stdev
from threading import Thread
import qpr_s4_scatter
import qpr_s4_median
import qpr_snr
import qpr_save_full_query

errorloglevel = logging.CRITICAL
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

com = mgr_comport.SerialManager(k.portName, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
timeformat = '%Y-%m-%d %H:%M:%S'
sat_database = "gps_satellites.db"
integration_time = 55
# duration = 60*60*24
# nullvalue = ""
logfiles = "logfiles"

# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 40

# This is the query output that will be used to generate graphs and plots etc.
querydata = []

# *************************************************
# Plotter and query processor thread
# *************************************************
class QueryProcessor(Thread):
    def __init__(self):
        Thread.__init__(self, name="QueryProcessor")

    def run(self):
        # put query data processing stuff here. NO matplot unfortunatly
        while True:
            print("***************************** Start Query Processor")
            try:
                qpr_save_full_query.wrapper(querydata)
            except:
                print("\n" + "!!!!!!!!!  Full Query Save Failed  !!!!!!!!!" + "\n")
                logging.warning("SNR failed in MAIN.PY")

            try:
                qpr_snr.wrapper(querydata)
            except:
                print("\n" + "!!!!!!!!!  SNR Failed  !!!!!!!!!" + "\n")
                logging.warning("SNR failed in MAIN.PY")

            try:
                qpr_s4_median.wrapper(querydata)
            except:
                print("\n" + "!!!!!!!!!  S4 Median Failed  !!!!!!!!!" + "\n")
                logging.warning("S4 Median failed in MAIN.PY")

            try:
                qpr_s4_scatter.wrapper(querydata)
            except:
                print("\n" + "!!!!!!!!!  S4 Scatter Failed  !!!!!!!!!" + "\n")
                logging.warning("S4 Scatter failed in MAIN.PY")

            # rings the terminal bell
            print("\a")
            print("******************************* End Query Processor")
            time.sleep(300)


class Satellite:
    def __init__(self, id):
        self.processflag = False
        self.id = id
        self.alt = []
        self.az = []
        self.snr = []
        self.intensity = []

    def get_s4(self):
        returnvalue = 0
        avg_intensity = mean(self.intensity)
        if len(self.intensity) > 2:
            sigma = stdev(self.intensity)
            if avg_intensity > 0:
                # variance = sigma * sigma
                # returnvalue = round((variance / avg_intensity), 5)
                returnvalue = round(((sigma / avg_intensity) * 100), 5)
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

    def get_intensity_avg(self):
        x = 0
        if len(self.intensity) > 0:
            x = mean(self.intensity)
        return x


def database_create():
    print("No database, creating file")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists satdata;')
    db.execute('create table satdata ('
               'sat_id text,'
               'posixtime integer,'
               'alt real,'
               'az real,'
               's4 real,'
               'snr real'
               ');')
    gpsdb.commit()
    db.close()


def posix2utc(posixtime):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def database_parse():
    starttime = int(time.time()) - (60 * 60 * 24)
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select sat_id, posixtime, alt, az, s4, snr from satdata where posixtime > ? and alt > ? order by posixtime asc', [starttime, optimum_altitude])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4], item[5])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


def nmea_sentence(sentence):
    s = sentence[1:]
    s = s.split("*")
    s = s[0].split(",")
    return s


def create_logfile_directory():
    try:
        os.makedirs(logfiles)
        print("Logfile directory created.")
    except:
        if not os.path.isdir(logfiles):
            print("Unable to create log directory")
            logging.critical("CRITICAL ERROR: Unable to create logs directory in MAIN.PY")


def calc_intensity(snr):
    snr = float(snr)
    intensity = 0
    if snr != 0:
        intensity = pow(10, (snr/10))
    return intensity


def satlist_input(gsv_sentence):
    constellation = gsv_sentence[0]
    increment = 4

    satlist = gpgsv
    if constellation == "glgsv":
        satlist = glgsv

    for i in range(4, len(gsv_sentence) - 3, increment):
        name = constellation + "_" + gsv_sentence[i]
        satID = int(gsv_sentence[i])
        alt = gsv_sentence[i + 1]
        az = gsv_sentence[i + 2]
        snr = gsv_sentence[i + 3]

        satlist[satID].id = name
        if alt == "":
            satlist[satID].alt.append(0)
        else:
            satlist[satID].alt.append(float(alt))

        if az == "":
            satlist[satID].az.append(0)
        else:
            satlist[satID].az.append(float(az))

        # at this step, add the value for intensity too
        if snr == "":
            satlist[satID].snr.append(0)
            satlist[satID].intensity.append(0)
        else:
            satlist[satID].snr.append(float(snr))
            i = calc_intensity(snr)
            satlist[satID].intensity.append(i)

        satlist[satID].processflag = True


if __name__ == "__main__":
    queryprocessor = QueryProcessor()
    try:
        queryprocessor.start()
        print("Starting query processor thread...")
    except:
        print("Unable to start database query processor thread in MAIN.PY!!")

    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(sat_database) is False:
        print("No database file, initialising")
        database_create()
    if os.path.isfile(sat_database) is True:
        print("Database file exists")

    if os.path.isdir(logfiles) is False:
        print("Creating log file directory...")
        create_logfile_directory()

    # Set up the lists required to average the satellite values so the DB
    # will store one minute values.
    gpgsv = []
    for i in range(0, 500):
        gpgsv.append(Satellite(i))

    glgsv = []

    for i in range(0, 500):
        glgsv.append(Satellite(i))

    counter = 0
    maxcounter = 180
    regex_expression = "(\$\w\wGSV),.+"

    while True:
        # Get com data
        line = com.data_recieve()

        # Parse com data for valid data GSV sentence ???GSV,
        if re.match(regex_expression, line):
            sentence = nmea_sentence(line)
            # make sure GSV sentence is a multiple of 4
            if len(sentence) % 4 == 0:
                try:
                    satlist_input(sentence)
                except:
                    print("There was a problem inputting satellite data inot the lists in MAIN.PY")
                counter = counter + 1

        # Process and reset things!
        if counter >= maxcounter:
            posixtime = int(time.time())
            for s in gpgsv:
                if s.processflag is True:
                    gpsdb = sqlite3.connect(sat_database)
                    db = gpsdb.cursor()
                    db.execute('insert into satdata (sat_id, posixtime, alt, az, s4, snr) values (?, ?, ?, ?, ?, ?);', [s.id, posixtime, s.get_alt_avg(), s.get_az_avg(), s.get_s4() ,s.get_snr_avg()])
                    gpsdb.commit()
                    db.close()

            for s in glgsv:
                if s.processflag is True:
                    gpsdb = sqlite3.connect(sat_database)
                    db = gpsdb.cursor()
                    db.execute('insert into satdata (sat_id, posixtime, alt, az, s4, snr) values (?, ?, ?, ?, ?, ?);', [s.id, posixtime, s.get_alt_avg(), s.get_az_avg(), s.get_s4() ,s.get_snr_avg()])
                    gpsdb.commit()
                    db.close()

            # *************************************************
            # Generate new query, reset counter.
            # *************************************************
            print("Creating output list from database...")
            querydata = database_parse()

            print("Resetting Satellite lists...")
            gpgsv = []
            for i in range(0, 500):
                gpgsv.append(Satellite(i))

            glgsv = []
            for i in range(0, 500):
                glgsv.append(Satellite(i))

            print("Reset counter...")
            counter = 0
            print("Done! " + posix2utc(posixtime) + "\n")
