import constants as k
import mgr_comport
import time
import os
import sqlite3
from statistics import mean, stdev, median
import datetime
import logging
import re
from matplotlib import pyplot as plt
import mgr_satellite_plotter
from matplotlib import ticker as ticker
import pickle


errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

com = mgr_comport.SerialManager(k.portName, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
timeformat = '%Y-%m-%d %H:%M'
sat_database = "gps_satellites.db"
integration_time = 55
duration = 60*60*24
nullvalue = ""
logfiles = "logfiles"
stdev_file = "stdev_test.pkl"


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
        snr = float(snr)
        intensity = 0
        if snr != 0:
            intensity = pow(10, (snr/10))
        return intensity

    def s4_index(self):
        returnvalue = 0

        if len(self.intensity) > self.min_array_len and sum(self.intensity) > 0:
            try:
                avg_intensity = mean(self.intensity)
                sigma = stdev(self.intensity)
                variance = sigma * sigma
                # returnvalue = round((variance / avg_intensity), 5)
                returnvalue = round(((sigma / avg_intensity) * 100), 5)
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
            result = round(mean(self.data), 4)
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

    result = db.execute('select sat_id, posixtime, alt, az, s4, snr from satdata where posixtime > ? and alt > 20 order by posixtime asc', [starttime])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4], item[5])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


def parse_database_constellation(const_name):
    constellation_searchstring = str(const_name)
    starttime = int(time.time()) - (60 * 60 * 24)
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()
    # result = db.execute(
    #     'select sat_id, posixtime, alt, az, s4 from satdata where posixtime > ? and alt > 20 order by posixtime asc',
    #     [starttime])
    criteria = [starttime, constellation_searchstring]
    result = db.execute("""select sat_id, posixtime, alt, az, s4 from satdata where posixtime > ? and alt > 20 and sat_id like ? order by posixtime asc""", criteria)
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


def store_sigma(stdev_value):
    stdev_list = []
    if os.path.isfile(stdev_file):
        stdev_list = pickle.load(open(stdev_file, "rb"))
    stdev_list.append(stdev_value)

    # list is larger than one carrington rotation, delete and append current mean, start again
    carrington_rotation = int((29 * 24 * 60 * 60) / integration_time)
    if len(stdev_list) > carrington_rotation:
        stdev_list.pop(0)
        stdev_list.append(stdev_value)
    print("STDev list is " + str(len(stdev_list)) + " " + str(carrington_rotation))
    pickle.dump(stdev_list, open(stdev_file, "wb"), 0)


def return_median_sigma():
    stdev_list = pickle.load(open(stdev_file, "rb"))
    returnvalue = median(stdev_list)
    print("STDev: " + str(returnvalue))
    return returnvalue


def create_s4_sigmas(resultlist):
    starttime = resultlist[0][1]
    endtime = resultlist[len(resultlist) - 1][1]
    # filename = "std_dev.csv"
    buckets = []

    # Set up the bin list
    if len(resultlist) > 180:
        for i in range(starttime, endtime, 60):
            buckets.append(BucketBin(i))
        # add data to each bins array
        for result in resultlist:
            index = int((result[1] - starttime) / 60) - 1
            buckets[index].data.append(result[4])

        #  write out the median of each bucket's data array to a new list
        templist = []
        for item in buckets:
            data = float(item.return_median())
            if data > 0:
                templist.append(data)

        minvalue = float(min(templist))
        sigma = round(float(stdev(templist)), 4)

        # Store the latest sigma in the list of sigmas
        store_sigma(sigma)
        # get the median value for the last 29 days
        sigma = return_median_sigma()

        # print(minvalue, sigma)

        returnlist = []
        for b in buckets:
            s_value = 0
            if b.return_median() == 0:
                data = nullvalue
            else:
                data = str(b.return_median())

                if float(data) >= (minvalue + sigma):
                    s_value = 2
                if float(data) >= (minvalue + (2 * sigma)):
                    s_value = 3

                if float(data) >= (minvalue + (3 * sigma)):
                    s_value = 4

                if float(data) >= (minvalue + (4 * sigma)):
                    s_value = 5

                if float(data) >= (minvalue + (5 * sigma)):
                    s_value = 6

                if float(data) >= (minvalue + (6 * sigma)):
                    s_value = 7

            dt = str(posix2utc(b.posixtime))
            dp = dt + "," + str(data) + "," + str(s_value)
            returnlist.append(dp)
        return returnlist


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
        ax.set_xlabel("Time UTC")
        ax.set_ylabel("S4 Index (%)", labelpad=5)
        s4.tight_layout()
        tic_space = 30
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_space))
        ax.tick_params(axis='x', labelrotation=90)
        plt.title("S4 Ionospheric Index")
        plt.savefig(savefile)
        plt.close('all')
        print("S4 plot created")
    except Exception:
        print("Unable to save image file")
    plt.close('all')


def create_logfile_directory():
    try:
        os.makedirs(logfiles)
        print("Logfile directory created.")
    except:
        if not os.path.isdir(logfiles):
            print("Unable to create log directory")
            logging.critical("CRITICAL ERROR: Unable to create logs directory")


def save_s4_file(resultlist, filename):
    try:
        with open(filename, 'w') as f:
            f.write("Datetime UTC, S4 Scintillation Index, Sigmas" + '\n')
            for result in resultlist:
                f.write(result + '\n')
        f.close()
        print("CSV file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(sat_database) is False:
        print("No database file, initialising")
        create_database()
    if os.path.isfile(sat_database) is True:
        print("Database file exists")

    if os.path.isdir(logfiles) is False:
        print("Creating log file directory...")
        create_logfile_directory()

    GPGSV = create_satellite_list("gps_")
    GLGSV = create_satellite_list("glonass_")
    GAGSV = create_satellite_list("galileo_")

    counter = 0
    regex_expression = "(\$\w\wGSV),.+"
    recordlength = 4
    runloop = True
    # main loop starts here run every second...
    posix_time = int(time.time())
    itercount = 0
    plotcounter = 0

    while runloop == True:
        # Get com data
        line = com.data_recieve()

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
            itercount = itercount + max_iter

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

            # after integration time has elapsed, get summarised data and S4 values fron satellites and append to database
            if time.time() >= posix_time + integration_time:
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

                if len(satellitelist) > 0:
                    for s in satellitelist:
                        print(s)
                    print(" ")
                    print("Satellite data processed: " + str(itercount) + " items.")
                else:
                    print(" WARNING - No Satellites being reported. Reboot Arduino??")
                    print("Exiting program - reinitialise the comport")
                    runloop = False

                ########################################################################################
                # THis was in a thread but pyplot is an arse. Should only consume a few seconds of time
                ########################################################################################
                resultlist = parse_database()
                # resultlist = parse_database_constellation("glonass%")
                # print(resultlist)

                # We recycle the create_sigmas function to generate a 24hr CSV logfile
                dt = posix2utc(posix_time).split(" ")
                name = dt[0] + "_test.csv"
                filepath = logfiles + "/" + name
                final_s4_list = create_s4_sigmas(resultlist)

                # CReate graphic plotfiles every 10 minutes.
                plotcounter = plotcounter + 1
                if plotcounter >= 10:
                    print("Creating matplot graphs!")
                    create_matplot(resultlist, 0, 100, "s4_scatter.png")
                    mgr_satellite_plotter.create_individual_plots(resultlist)
                    plotcounter = 0

                try:
                    save_s4_file(final_s4_list, filepath)
                    save_s4_file(final_s4_list, "std_dev2_test.csv")
                except TypeError:
                    print("S4 file not large enough to process just yet")

                # finally...
                posix_time = int(time.time())
                print("Completed task at: " + posix2utc(posix_time) + "\n")
                itercount = 0

