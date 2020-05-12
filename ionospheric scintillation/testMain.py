import constants as k
import mgr_comport
import time
from threading import Thread
import os
import sqlite3
from statistics import mean, stdev
import datetime

com = mgr_comport.SerialManager(k.portName,k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
timeformat = '%Y-%m-%d %H:%M:%S'
sat_database = "gps_satellites.db"

# db = gpsdb.cursor()

class GPSSatellite:
    def __init__(self, sat_name):
        self.name = sat_name
        self.posixtime = ''
        self.alt = []
        self.az = []
        self.intensity = []

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
        if len(self.alt) > 2:
            returnvalue = round(mean(self.alt), 3)
        return returnvalue

    def return_az(self):
        returnvalue = 0
        if len(self.az) > 2:
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
        if sum(self.intensity) > 0:
            avg_intensity = mean(self.intensity)
            sigma = stdev(self.intensity)
            returnvalue = round((sigma / avg_intensity), 3)
        return returnvalue

    def reset(self):
        self.posixtime = ''
        self.alt = []
        self.az = []
        self.intensity = []


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


class SatelliteCollator(Thread):
    def __init__(self):
        Thread.__init__(self, name="SatelliteCollator")

    def run(self):
        while True:
            resultlist = parse_database()
            create_csv(resultlist)
            time.sleep(60*5)


def create_database():
    print("No database, creating file")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists satdata;')
    msg = db.execute('create table satdata ('
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
    starttime = int(time.time()) - 60*60*24
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


if __name__ == "__main__":
    # will create the database if it exists
    if os.path.isfile(sat_database) is False:
        print("No database file, initialising")
        create_database()
    if os.path.isfile(sat_database) is True:
        print("Database file exists")

    # create_database()
    counter = 0

    GPGSV = []
    for i in range(0, 101):
        name = 'gps_' + str(i)
        gps = GPSSatellite(name)
        GPGSV.append(gps)

    GLGSV = []
    for i in range(0, 101):
        name = 'glonass_' + str(i)
        gps = GPSSatellite(name)
        GLGSV.append(gps)

    sat_collation = SatelliteCollator()
    try:
        sat_collation.start()
    except:
        print("Unable to start Satellite Collator")

    print("Starting GPS collection...")

    recordlength = 4
    while True:
        counter = counter + 1
        posix_time = int(time.time())

        line = com.data_recieve()

        sentence = nmea_sentence(line)
        constellation = sentence[0]
        s_id = 4
        s_alt = 5
        s_az = 6
        s_snr = 7

        # to determine how many records there are in the sentence. Minus the 4 slots at the front, div by four
        # to create the range for the FOR loop
        max_iter = int(((len(sentence) - 4) / 4) )

        # only if we have a sentence long enough
        if len(sentence) > recordlength + 4:
            for i in range(0, max_iter):
                # Append current sentence to a satellite
                # print(posix_time, constellation + "_" + sentence[s_id], sentence[s_alt], sentence[s_az],sentence[s_snr])
                index_value = int(sentence[s_id])
                if constellation == "GPGSV":
                    GPGSV[index_value].posixtime = posix_time
                    GPGSV[index_value].set_alt(sentence[s_alt])
                    GPGSV[index_value].set_az(sentence[s_az])
                    GPGSV[index_value].set_intensity(sentence[s_snr])

                if constellation == "GLGSV":
                    GLGSV[index_value].posixtime = posix_time
                    GLGSV[index_value].set_alt(sentence[s_alt])
                    GLGSV[index_value].set_az(sentence[s_az])
                    GLGSV[index_value].set_intensity(sentence[s_snr])

                # Grab the next satellite in the sentence
                s_id = s_id + recordlength
                s_alt = s_alt + recordlength
                s_az = s_az + recordlength
                s_snr = s_snr + recordlength

        if counter >= 600:
            satellitelist = []
            for sat in GPGSV:
                if sat.s4_index() > 0:
                    satellitelist.append((sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index()))
                    # Store the satellite data to the database, once per minute
                    gpsdb = sqlite3.connect(sat_database)
                    db = gpsdb.cursor()
                    db.execute('insert into satdata (sat_id, posixtime, alt, az, s4) values (?, ?, ?, ?, ?);',[sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index()])
                    gpsdb.commit()
                    db.close()

            for sat in GLGSV:
                if sat.s4_index() > 0:
                    satellitelist.append((sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index()))
                    # Store the satellite data to the database, once per minute
                    gpsdb = sqlite3.connect(sat_database)
                    db = gpsdb.cursor()
                    db.execute('insert into satdata (sat_id, posixtime, alt, az, s4) values (?, ?, ?, ?, ?);',[sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index()])
                    gpsdb.commit()
                    db.close()

            for sat in GPGSV:
                sat.reset()

            for sat in GLGSV:
                sat.reset()

            counter = 0
            for s in satellitelist:
                print(s)
            print(" ")

