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
integration_time = 60
duration = 60*60*24
nullvalue = ""


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
        self.snr = []
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

    def set_snr(self, value):
        if value == '':
            appendvalue = 0
        else:
            appendvalue = int(value)
        self.snr.append(appendvalue)

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

    def return_snr(self):
        returnvalue = 0
        if len(self.snr) > self.min_array_len:
            returnvalue = round(mean(self.snr), 5)
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


class BucketBin:
    def __init__(self, posixtime):
        self.posixtime = posixtime
        self.data = []

    def return_median(self):
        # print(self.data)
        result = 0
        if len(self.data) > 0:
            result =  round(mean(self.data), 4)
        return result


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


def parse_database():
    starttime = int(time.time()) - (60 * 60 * 24)
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select sat_id, posixtime, alt, az, s4 from satdata where posixtime > ? and alt > 20 order by posixtime asc', [starttime])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


def parse_snr():
    starttime = int(time.time()) - duration
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select sat_id, posixtime, alt, az, snr from satdata where posixtime > ? and alt > 20', [starttime])
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
    filename = "s4.csv"
    try:
        with open(filename, 'w') as f:
            for result in resultlist:
                if result[4] == 0:
                    data = nullvalue
                else:
                    data = result[4]
                dt = posix2utc(result[1])
                dp = str(dt + "," + data)
                f.write(dp + '\n')
        f.close()
        print("CSV file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")


def create_s4_line(resultlist):
    starttime = resultlist[0][1]
    endtime = resultlist[len(resultlist) - 1][1]
    filename = "linechart.csv"
    buckets = []

    # Set up the bin list
    if len(resultlist) > 180:
        for i in range(starttime, endtime, 60):
            buckets.append(BucketBin(i))
        # add data to each bins array
        for result in resultlist:
            index = int((result[1] - starttime) / 60)
            buckets[index].data.append(result[4])
        #  write out the median of each bucket's data array to a new list
        returnlist = []
        for b in buckets:
            if b.return_median() == 0:
                data = nullvalue
            else:
                data = str(b.return_median())
            dt = str(posix2utc(b.posixtime))
            dp = dt + "," + data
            returnlist.append(dp)

        try:
            with open(filename, 'w') as f:
                for result in returnlist:
                    f.write(result + '\n')
            f.close()
            print("CSV file written")
        except PermissionError:
            print("CSV file being used by another app. Update next time")

def create_s4_sigmas(resultlist):
    starttime = resultlist[0][1]
    endtime = resultlist[len(resultlist) - 1][1]
    filename = "std_dev.csv"
    buckets = []

    # Set up the bin list
    if len(resultlist) > 180:
        for i in range(starttime, endtime, 60):
            buckets.append(BucketBin(i))
        # add data to each bins array
        for result in resultlist:
            index = int((result[1] - starttime) / 60)
            buckets[index].data.append(result[4])
        #  write out the median of each bucket's data array to a new list

        templist = []
        for item in buckets:
            templist.append(item.return_median())
        minvalue = min(templist)
        sigma = stdev(templist)

        returnlist = []
        for b in buckets:
            s1, s2, s3, s4 = 0, 0, 0, 0
            if b.return_median() == 0:
                data = nullvalue
            else:
                data = str(b.return_median())

                if float(data) > minvalue + sigma:
                    s1 = 1
                elif float(data) > (minvalue + sigma) and float(data) < (minvalue + 2 * sigma):
                    s2 = 2
                elif float(data) > (minvalue + 2 * sigma) and float(data) < (minvalue + 3 * sigma):
                    s3 = 3
                elif float(data) > (minvalue + 3 * sigma):
                    s4 = 4

            dt = str(posix2utc(b.posixtime))
            dp = dt + "," + str(data) + "," + str(s1) + "," + str(s2) + "," + str(s3) + "," + str(s4)
            returnlist.append(dp)

        try:
            with open(filename, 'w') as f:
                for result in returnlist:
                    f.write(result + '\n')
            f.close()
            print("CSV file written")
        except PermissionError:
            print("CSV file being used by another app. Update next time")


# def create_s4_dxdt(resultlist):
#     starttime = resultlist[0][1]
#     endtime = resultlist[len(resultlist) - 1][1]
#     filename = "s4_dxdt.csv"
#     halfwindow = 40
#     buckets = []
#
#     # Set up the bin list
#     if len(resultlist) > 180:
#         for i in range(starttime, endtime, 60):
#             buckets.append(BucketBin(i))
#         # add data to each bins array
#         for result in resultlist:
#             index = int((result[1] - starttime) / 60)
#             buckets[index].data.append(result[4])
#
#         #  write out the median of each bucket's data array to a new list
#         t1 = []
#         for b in buckets:
#             dp = [b.posixtime, b.return_median()]
#             t1.append(dp)
#
#         # calculate dx/dt
#         t2 = []
#         for i in range (1, len(t1)):
#             dt = t1[i][0]
#             dx = t1[i][1] - t1[i-1][1]
#             dp = [dt, dx]
#             t2.append(dp)
#
#         # Smooth dxdt
#         t3 = []
#         for i in range(halfwindow, len(t2) - 1 - halfwindow):
#             avg = []
#             dt = t2[i][0]
#             for j in range(halfwindow * -1, halfwindow):
#                 data = t2[i + j][1]
#                 avg.append(data)
#             avg_data = mean(avg)
#             dp = [dt, avg_data]
#             t3.append(dp)
#
#         try:
#             with open(filename, 'w') as f:
#                 for result in t3:
#                     f.write(posix2utc(result[0]) + "," + str(result[1]) + '\n')
#             f.close()
#             print("CSV file written")
#         except PermissionError:
#             print("CSV file being used by another app. Update next time")


# def create_snr(resultlist):
#     filename = "snr.csv"
#     try:
#         with open(filename, 'w') as f:
#             for result in resultlist:
#                 dp = str(result[0]) + "," + str(posix2utc(result[1])) + "," +  str(result[2]) + "," +  str(result[3]) + "," +  str(result[4])
#                 f.write(dp + '\n')
#         f.close()
#         print("CSV file written")
#     except PermissionError:
#         print("CSV file being used by another app. Update next time")


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
        ax.scatter(x, y, marker="o", s=9, alpha=0.1, color=['black'])
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
        print("Unable to save image file")
        plt.close('all')


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
    runloop = True
    # main loop starts here run every second...
    while runloop == True:
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
                            GPGSV[index_value].set_snr(sentence[s_snr])
                            GPGSV[index_value].set_intensity(sentence[s_snr])

                        if constellation == "GLGSV":
                            GLGSV[index_value].posixtime = posix_time
                            GLGSV[index_value].set_alt(sentence[s_alt])
                            GLGSV[index_value].set_az(sentence[s_az])
                            GLGSV[index_value].set_snr(sentence[s_snr])
                            GLGSV[index_value].set_intensity(sentence[s_snr])

                        if constellation == "GAGSV":
                            GAGSV[index_value].posixtime = posix_time
                            GAGSV[index_value].set_alt(sentence[s_alt])
                            GAGSV[index_value].set_az(sentence[s_az])
                            GAGSV[index_value].set_snr(sentence[s_snr])
                            GAGSV[index_value].set_intensity(sentence[s_snr])

                    except ValueError:
                        logging.debug("DEBUG: String as integer in satellite ID: " + str(sentence[s_id]))

                    # Grab the next satellite in the sentence
                    s_id = s_id + recordlength
                    s_alt = s_alt + recordlength
                    s_az = s_az + recordlength
                    s_snr = s_snr + recordlength


            # after 60 seconds, get summarised data and S4 values fron satellites and append to database
            if counter >= integration_time:
                satellitelist = []
                for sat in GPGSV:
                    if sat.s4_index() > 0:
                        satellitelist.append((sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index(), sat.return_snr()))
                        # Store the satellite data to the database, once per minute
                        gpsdb = sqlite3.connect(sat_database)
                        db = gpsdb.cursor()
                        db.execute('insert into satdata (sat_id, posixtime, alt, az, s4, snr) values (?, ?, ?, ?, ?, ?);',[sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index(), sat.return_snr()])
                        gpsdb.commit()
                        db.close()

                for sat in GLGSV:
                    if sat.s4_index() > 0:
                        satellitelist.append((sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index(), sat.return_snr()))
                        # Store the satellite data to the database, once per minute
                        gpsdb = sqlite3.connect(sat_database)
                        db = gpsdb.cursor()
                        db.execute('insert into satdata (sat_id, posixtime, alt, az, s4, snr) values (?, ?, ?, ?, ?, ?);',[sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index(), sat.return_snr()])
                        gpsdb.commit()
                        db.close()

                for sat in GAGSV:
                    if sat.s4_index() > 0:
                        satellitelist.append((sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index(), sat.return_snr()))
                        # Store the satellite data to the database, once per minute
                        gpsdb = sqlite3.connect(sat_database)
                        db = gpsdb.cursor()
                        db.execute('insert into satdata (sat_id, posixtime, alt, az, s4, snr) values (?, ?, ?, ?, ?, ?);',[sat.name, sat.posixtime, sat.return_alt(), sat.return_az(), sat.s4_index(), sat.return_snr()])
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

                if len(satellitelist) > 0:
                    for s in satellitelist:
                        print(s)
                    print(" ")
                else:
                    print(" WARNING - No Satellites being reported. Reboot Arduino??")
                    print("Exiting program - reinitialise the comport")
                    runloop = False

                ########################################################################################
                # THis was in a thread but pyplot is an arse. Should only consume a few seconds of time
                ########################################################################################
                resultlist = parse_database()
                snr_list = parse_snr()

                # create_csv(resultlist)
                create_s4_line(resultlist)
                create_s4_sigmas(resultlist)
                # create_s4_dxdt(resultlist)
                # create_snr(snr_list)

                # create_matplot(resultlist, 0, 5, "s4_12.png")
                create_matplot(resultlist, 0, 1, "s4_01.png")
                # create_matplot(resultlist, 0, 0.25, "s4_02.png")
                # create_matplot(resultlist, 0.1, 0.13, "line.png")
                print("Done!")
