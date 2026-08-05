"""
This program creates 24hour logfiles. These are saved independent of any database
"""
import sqlite3
import constants as k
import logging
import time
import datetime
import os
from statistics import mean
"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.WARNING
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
timeformat = '%Y-%m-%d %H:%M:%S'
# stations = ["Ruru_Obs", "GOES_16", "Geomag_Bz", "SW_speed", "SW_Density"]
stations = k.stations
finish_time = int(time.time())
start_time = finish_time - (60 * 60 * 24)
binsize = 60
number_bins = int((finish_time - start_time) / binsize) + 2
null_value = " "

class DataPoint():
    def __init__(self, timevalue):
        self.datalist = []
        self.timevalue = timevalue

    def avg_data(self):
        if len(self.datalist) > 0:
            return mean(self.datalist)
        else:
            return null_value


def posix2utc(posixvalue):
    # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime(timeformat)
    return utctime


def bin_indexvalue(nowtime):
    returnvalue = int((int(nowtime) - start_time) / binsize)
    return returnvalue


def check_create_folders():
    for station in stations:
        try:
            if not os.path.exists(station):
                print("Create directory for " + station)
                os.makedirs(station)
            else:
                print("Directory exists for " + station)
        except Exception:
            print("Some kind of error happened creating the directory for " + station)


def save_logfiles():
    # result = db.execute("select station_data.posix_time, station_data.data_value from station_data")
    # print(result.fetchall())
    for station in stations:
        datapoint_list = []
        timestamp = start_time
        for i in range(0, number_bins):
            dp = DataPoint(timestamp)
            datapoint_list.append(dp)
            timestamp = timestamp + binsize

        result = db.execute("select station_data.posix_time, station_data.data_value from station_data "
                            "where station_data.station_id = ? and station_data.posix_time > ?", [station, start_time])

        current_stationdata = result.fetchall()

        # Setup for saving basic log files
        savefile = station + "//" + datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d') + ".csv"
        nowfile = station + ".csv"
        tempfile = []
        header = station + ", data"
        tempfile.append(header)

        for item in current_stationdata:
            date = posix2utc(item[0])
            data = item[1]
            dp = date + "," + data
            tempfile.append(dp)

        with open(savefile, "w") as s:
            for item in tempfile:
                s.write(item + "\n")
        s.close()

        # Bin the data into one minute bins then save
        for item in current_stationdata:
            try:
                index = bin_indexvalue(item[0])
                data = float(item[1])
                datapoint_list[index].datalist.append(data)
            except IndexError:
                print("Index error in datapoint list")

        binned_data = []
        header = station + ", data"
        binned_data.append(header)
        for item in datapoint_list:
            timevalue = item.timevalue
            datavalue = item.avg_data()
            dp = str(posix2utc(timevalue)) + ", " + str(datavalue)
            binned_data.append(dp)

        with open(nowfile, "w") as n:
            for item in binned_data:
                n.write(item + "\n")
        n.close()


if __name__ == "__main__":
    check_create_folders()
    save_logfiles()

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
