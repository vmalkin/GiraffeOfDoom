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


errorloglevel = logging.CRITICAL
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

com = mgr_comport.SerialManager(k.portName, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
timeformat = '%Y-%m-%d %H:%M:%S'
sat_database = "gps_satellites.db"
integration_time = 30
# duration = 60*60*24
# nullvalue = ""
s4_interval = 24 * 10

# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 25

# This is the query output that will be used to generate graphs and plots etc.
querydata_24 = []
# querydata_48 = []
current_stats = []


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
                logging.warning("SNR failed in MAIN.PY")

            try:
                mgr_polar_s4_noise.wrapper(querydata_24)
            except:
                print("\n" + "mgr_polar_s4_noise.wrapper" + "\n")
                logging.warning("satellite plotter failed in MAIN.PY")

            try:
                mgr_polar_noise_tracks.wrapper(querydata_24)
            except:
                print("\n" + "mgr_polar_noise_tracks.wrapper" + "\n")
                logging.warning("satellite plotter failed in MAIN.PY")

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
        self.intensity = []

    def get_s4(self):
        # http://mtc-m21b.sid.inpe.br/col/sid.inpe.br/mtc-m21b/2017/08.25.17.52/doc/poster_ionik%20%5BSomente%20leitura%5D.pdf
        returnvalue = 0
        if len(self.intensity) > 2:
            avg_intensity = mean(self.intensity)
            sigma = stdev(self.intensity)
            if avg_intensity > 0:
                returnvalue = round(((sigma / avg_intensity) * 100), 5)

        return returnvalue

    def get_alt_avg(self):
        x = 0
        if len(self.alt) > 0:
            x = median(self.alt)
        return x

    def get_az_avg(self):
        x = 0
        if len(self.az) > 0:
            x = median(self.az)
        return x

    def get_snr_avg(self):
        x = 0
        if len(self.snr) > 0:
            x = median(self.snr)
        return x

    def get_intensity_avg(self):
        x = 0
        if len(self.intensity) > 0:
            x = median(self.intensity)
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


def database_parse(hourduration):
    starttime = int(time.time()) - (60 * 60 * hourduration)
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


def create_directory(dir):
    try:
        os.makedirs(dir)
        print("Directory created.")
    except:
        if not os.path.isdir(dir):
            print("Unable to create directory")
            logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")


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
        # needed as occasional cruft seems to be attached to this value and we need it to be an int
        id = gsv_sentence[i]
        id = id.strip()
        if id[:1] == "0":
            id = id[1:]
        id = id + ".0"
        id = int(float(id))
        
        name = constellation + "_" + str(id)
        satID = (id)
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

    if os.path.isdir(k.dir_logfiles) is False:
        print("Creating log file directory...")
        create_directory(k.dir_logfiles)

    if os.path.isdir(k.dir_images) is False:
        print("Creating image file directory...")
        create_directory(k.dir_images)

    # Set up the lists required to average the satellite values so the DB
    # will store one minute values.
    gpgsv = []
    for i in range(0, 500):
        gpgsv.append(Satellite(i))

    glgsv = []
    for i in range(0, 500):
        glgsv.append(Satellite(i))

    oldtimer = time.time()
    counter = 0
    maxcounter = 300
    regex_expression = "(\$\w\wGSV),.+"

    while True:
        # Get com data_s4
        line = com.data_recieve()
        # print(line[:6])

        # Parse com data_s4 for valid data_s4 GSV sentence ???GSV,
        # if re.match(regex_expression, line):
        # if line[:6] == "$GPGSV":
        if line[:6] == "$GPGSV" or line[:6] == "$GLGSV":
            sentence = nmea_sentence(line)
            # make sure GSV sentence is a multiple of 4
            if len(sentence) % 4 == 0:
                try:
                    satlist_input(sentence)
                except:
                    print("There was a problem inputting satellite data_s4 into the lists in MAIN.PY")
                    print(sentence)
                counter = counter + 1
        # else:
        #     # print("Sentence did not pass regex")
        #     # print(line)


        # Process and reset things!
        nowtimer = time.time()
        # at least one minute has elapsed
        if nowtimer >= (oldtimer + 60):
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
            querydata_24 = database_parse(24)
            querydata_48 = database_parse(48)

            print("Resetting Satellite lists...")
            gpgsv = []
            for i in range(0, 500):
                gpgsv.append(Satellite(i))

            glgsv = []
            for i in range(0, 500):
                glgsv.append(Satellite(i))

            print("Satellite readings processed: " + str(counter))
            counter = 0
            oldtimer = nowtimer
            print("Done! " + posix2utc(posixtime) + "\n\n")
