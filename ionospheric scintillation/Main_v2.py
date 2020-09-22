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
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker


errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

com = mgr_comport.SerialManager(k.portName,k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
# timeformat = '%Y-%m-%d %H:%M:%S'
timeformat = '%Y-%m-%d %H:%M'
sat_database = "gps_satellites.db"


# class SatelliteCollator(Thread):
#     def __init__(self):
#         Thread.__init__(self, name="SatelliteCollator")
#
#     def run(self):
#         while True:
#             resultlist = parse_database()
#             create_csv(resultlist)
#             create_matplot(resultlist, 0, 1, "s4_1.png")
#             # create_matplot(resultlist, 0.5, "s4_05.png")
#             create_matplot(resultlist, 0, 0.2, "s4_02.png")
#             create_matplot(resultlist, 0.1, 0.14, "line.png")
#             time.sleep(60*5)


class GPSSatellite:
    def __init__(self, sat_name):
        self.name = sat_name
        self.posixtime = ''
        self.alt = []
        self.az = []
        self.intensity = []
        self.min_array_len = 3

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
            returnvalue = round(mean(self.alt), 5)
        return returnvalue

    def return_az(self):
        returnvalue = 0
        if len(self.az) > self.min_array_len:
            returnvalue = round(mean(self.az), 5)
        return returnvalue

    def calc_intensity(self, snr):
        snr = int(snr)
        intensity = 0
        if snr != 0:
            intensity = pow(10, (snr/10))
        return intensity

    def s4_index(self):
        # print(self.intensity)
        returnvalue = 0

        if len(self.intensity) > self.min_array_len and sum(self.intensity) > 0:
            try:
                # self.intensity = [2,5,5,8,8,8,11,11,14]
                # sI2s = float(0)
                # sIs2 = float(0)
                # for i in self.intensity:
                #     sI2s = sI2s + (i*i)
                #
                # sIs2 = pow(sum(self.intensity), 2)
                #
                # s4 = (sI2s - sIs2) / sIs2
                # # s4 = round(sqrt(s4), 3)
                # print(s4)
                # returnvalue = s4
                avg_intensity = mean(self.intensity)
                sigma = stdev(self.intensity)
                returnvalue = round((sigma / avg_intensity), 5)
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
    for i in range(0, 300):
        name = constellationname + str(i)
        gps = GPSSatellite(name)
        returnlist.append(gps)
    return returnlist


def create_matplot(resultlist, ylow, ymax, filename):
    savefile = filename
    ylow = ylow
    ymax = ymax
    x = []
    y = []

    for line in resultlist:
        x_val = posix2utc(line[1])
        y_val = line[4]
        x.append(x_val)
        y.append(y_val)
    try:
        s4, ax = plt.subplots(figsize=[20, 9], dpi=100)
        ax.scatter(x, y, alpha=0.1, color=['black'])
        ax.set_ylim(ylow, ymax)
        ax.grid(True, color="#ccb3b3")

        tic_space = 30
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_space))

        ax.tick_params(axis='x', labelrotation=90)
        ax.set_xlabel("Time UTC")
        ax.set_ylabel("S4 Index", labelpad=5)
        s4.tight_layout()

        # plt.show()
        # plt.xlabel("Time, UTC")
        # plt.ylabel("S4 index values")
        plt.title("S4 Ionospheric Index")
        plt.savefig(savefile)
        plt.close('all')
        print("S4 plot created")
    except Exception:
        print("Unable to save file")


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

    # # begin graphing thread
    # sat_collation = SatelliteCollator()
    # try:
    #     sat_collation.start()
    # except:
    #     print("Unable to start Satellite Collator")

    counter = 0
    regex_expression = "(\$\w\wGSV),.+"
    recordlength = 4

    # main loop starts here run every second...
    while True:
        posix_time = int(time.time())

        # Get com data
        line = com.data_recieve()

        counter = counter + 1
        # print(counter)
        # print(line)
        # Parse com data for valid data GSV sentence ???GSV,
        if re.match(regex_expression, line):
            # print(line)
            # GSV sentence, parse out the satellite data
            sentence = nmea_sentence(line)
            constellation = sentence[0]
            s_id = 4
            s_alt = 5
            s_az = 6
            s_snr = 7
            max_iter = int(((len(sentence) - 4) / 4))

            # if valid data, sppend to satellite in lists
            if len(sentence) > recordlength + 4:
                for i in range(0, max_iter):
                    # Append current sentence to a satellite
                    # print(posix_time, constellation + "_" + sentence[s_id], sentence[s_alt], sentence[s_az],sentence[s_snr])
                    try:
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

                        if constellation == "GAGSV":
                            GAGSV[index_value].posixtime = posix_time
                            GAGSV[index_value].set_alt(sentence[s_alt])
                            GAGSV[index_value].set_az(sentence[s_az])
                            GAGSV[index_value].set_intensity(sentence[s_snr])

                    except ValueError:
                        logging.debug("DEBUG: String as integer in satellite ID: " + str(sentence[s_id]))

                    # Grab the next satellite in the sentence
                    s_id = s_id + recordlength
                    s_alt = s_alt + recordlength
                    s_az = s_az + recordlength
                    s_snr = s_snr + recordlength


            # after 60 seconds, get summarised data and S4 values fron satellites and append to database
            if counter >= 60*4:
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

                for sat in GAGSV:
                    if sat.s4_index() > 0:
                        satellitelist.append((sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index()))
                        # Store the satellite data to the database, once per minute
                        gpsdb = sqlite3.connect(sat_database)
                        db = gpsdb.cursor()
                        db.execute('insert into satdata (sat_id, posixtime, alt, az, s4) values (?, ?, ?, ?, ?);',[sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index()])
                        gpsdb.commit()
                        db.close()

                # reset satellite lists
                for sat in GPGSV:
                    sat.reset()

                for sat in GLGSV:
                    sat.reset()

                for sat in GAGSV:
                    sat.reset()

                counter = 0
                for s in satellitelist:
                    print(s)
                print(" ")

                # THis was in a thread but pyplot is an arse. Should only consume a few seconds of time
                resultlist = parse_database()
                create_csv(resultlist)
                create_matplot(resultlist, 0, 5, "s4_12.png")
                create_matplot(resultlist, 0, 1, "s4_01.png")
                create_matplot(resultlist, 0, 0.25, "s4_02.png")
                create_matplot(resultlist, 0.1, 0.13, "line.png")
                print("Done!")

