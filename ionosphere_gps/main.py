import math
import constants as k
import mgr_comport
import time
import os
import logging
from threading import Thread
import re
import standard_stuff
import random
import mgr_plotter
# from datetime import datetime
# from calendar import timegm
import mgr_database


errorloglevel = logging.ERROR
logging.basicConfig(filename="gnss.log", format='%(asctime)s %(message)s', level=errorloglevel)
random.seed()
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
            print('Plot last hour GPS tracks')
            last_6_hours = time.time() - (60 * 60 * 1)
            query_result = mgr_database.db_get_gsv(last_6_hours)
            mgr_plotter.polarplot_paths(query_result)

            print('Plot SNR')
            start = time.time() - (60 * 60 * 24 * 3)
            query_result = mgr_database.db_get_snr(start)
            mgr_plotter.basicplot(query_result)

            print('Plot satellite SNRs')
            start = time.time() - (60 * 60 * 24)
            query_result = mgr_database.db_get_gsv(start)
            mgr_plotter.plot_multi_snr(query_result)

            print('latest_sats.txt updated with latest sighting time')
            query_result = mgr_database.db_get_latest_sats()
            savefile = k.dir_images + os.sep + 'latest_sats.txt'
            with open(savefile, 'w') as l:
                for item in query_result:
                    name = item[0]
                    date = standard_stuff.posix2utc(item[1], '%Y-%m-%d %H:%M')
                    dp = name + ',' + date + '\n'
                    l.write(dp)
            l.close()


            # Get data for each constellation.
            # result = mgr_database.qry_get_last_24hrs(start_time, "GPGGA")
            # mgr_plot.wrapper(result, "GPS")

            print("******************************* End Query Processor")
            wiggle = random.randint(-180, 180)
            sleeptime = (60 * 15) + wiggle
            print('Next plot in ' + str(sleeptime) + ' seconds.')
            time.sleep((sleeptime))


def get_rounded_posix_():
    t = time.time()
    t = math.floor(t)
    return t


def create_directory(directory):
    try:
        os.makedirs(directory)
        print("Directory created.")
    except:
        if not os.path.isdir(directory):
            print("Unable to create directory")
            logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")


def parse_msg_id(msgid):
    # print(msgid)
    id_ok = False
    valid_id = ['$GPGSV', '$GPGGA']
    # valid_id = ['$GPGSV', '$GPGGA', '$GPRMC']
    for item in valid_id:
        if msgid == item:
            id_ok = True
    return id_ok


def process_gsv(gsv_data):
    mgr_database.db_gpgsv_add(gsv_data)

def shorten_gsv(csv_line):
    # only leave id, alt, az, snr data for each satellite
    satdata = csv_line[4:-1]
    return satdata


def add_satellites(gsv_collection, current_posixtime, gsv):
    if len(gsv) % 4 == 0:
        for i in range(0, len(gsv), 4):
            parsed_data = []
            parsed_data.append(current_posixtime)
            single_data = gsv[i: i + 4]
            # print(single_data)
            for item in single_data:
                parsed_data.append(item)
            gsv_collection.append(parsed_data)
    # print(" ")
    return  gsv_collection


if __name__ == "__main__":
    # initial setup including satellite lists
    # if database not exists, create database
    if os.path.isfile(k.sat_database) is False:
        print("No database file, initialising")
        mgr_database.db_create()

        # init with default values in tables.
        mgr_database.db_initialise()

    if os.path.isfile(k.sat_database) is True:
        print("Database file exists")

    if os.path.isdir(k.dir_images) is False:
        print("Creating image file directory...")
        create_directory(k.dir_images)

    queryprocessor = QueryProcessor()
    queryprocessor.start()

    com = mgr_comport.SerialManager(k.comport, k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout,
                                    k.xonxoff,
                                    k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)
    gsv_collection = []
    while True:
        current_posixtime = get_rounded_posix_()
        # Get com data
        # ['$GPGSV', '3', '1', '12', '05', '16', '108', '31', '10', '29', '278', '17', '13', '29', '132', '39', '15', '58', '110', '32', '7B']
        # ['$GPRMC', '002841.00', 'A', '4551.95891', 'S', '17031.19120', 'E', '0.091', '', '080224', '', '', 'D', '65']
        #  ['$GPGGA', '002841.00', '4551.95891', 'S', '17031.19120', 'E', '2', '06', '10.32', '23.7', 'M', '1.8', 'M', '', '0000', '72']
        # typical nmea messages
        line = com.data_recieve()
        csv_line = re.split(r'[,|*]', line)
        msg_id = csv_line[0]

        # if a valid NMEA message ID
        if parse_msg_id(msg_id) is True :
            # if msg_id == '$GPGGA':
            if msg_id == '$GPGSV':
                gsv = shorten_gsv(csv_line)
                # print(line)
                gsv_collection = add_satellites(gsv_collection, current_posixtime, gsv)
                # Once our collection of gsv data is large enough, process.
                # This delay reduces the risk of the database being locked for charting
                if len(gsv_collection) >= 3000:
                    process_gsv(gsv_collection)
                    gsv_collection = []
                    now = standard_stuff.posix2utc(current_posixtime, '%Y-%m-%d %H:%M')
                    print(now, "GSV data added.")
        # ENTER into database
