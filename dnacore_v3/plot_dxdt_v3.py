import sqlite3
import constants as k
import logging
import time
import datetime
import os
from statistics import mean, median, stdev
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

# Only specific station data makes sense as detrended readings.
stations = ["Ruru_Obs", "GOES_16"]
# stations = ["GOES_16", "Ruru_Obs"]
# stations = k.stations

finish_time = int(time.time())
start_time = finish_time - (60 * 60 * 24)
binsize = 60 * 60
number_bins = int((finish_time - start_time) / binsize) + 2
null_value = ""
half_window = 90


class DataPoint:
    def __init__(self, timevalue):
        self.datalist = []
        self.timevalue = timevalue

    def avg_data(self):
        if len(self.datalist) > 0:
            return float(mean(self.datalist))
        else:
            return null_value

    def max_data(self):
        if len(self.datalist) > 0:
            return float(max(self.datalist))
        else:
            return 0

    def min_data(self):
        if len(self.datalist) > 0:
            return float(min(self.datalist))
        else:
            return 0


def filter_median(list):
    """Takes in a list of DataPoints and performs a median filter on the object's datavalue"""
    filterwindow = 3
    returnlist = []
    for i in range(filterwindow, len(list)):
        medianstore = []
        datetime = list[i][0]
        for j in range(0, filterwindow):
            k = i - j
            datavalue = list[k][1]
            medianstore.append(datavalue)

        if len(medianstore) > 0:
            data = median(medianstore)
            dp = (datetime, data)
            returnlist.append(dp)
    return returnlist


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


def get_data(station):
    result = db.execute("select station_data.posix_time, station_data.data_value from station_data "
                        "where station_data.station_id = ? and station_data.posix_time > ?", [station, start_time])
    query_result = result.fetchall()
    return query_result


def posix2utc(posixtime):
    # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def parse_querydata(querydata):
    # turn the readings into rate of change.
    tempdata = []
    for i in range(1, len(querydata)):
        date = int(querydata[i][0])
        newdata = float(querydata[i][1])
        dp = (date, newdata)
        tempdata.append(dp)
    return tempdata


def save_logfiles(filename, datalist):
    with open(filename, "w") as n:
        for item in datalist:
            da = str(item[0])
            dt = str(item[1])
            dp = da + "," + dt + "\n"
            n.write(dp)
    n.close()


def bin_data(tempdata):
    datapoint_list = []
    timestamp = start_time
    for i in range(0, number_bins):
        dp = DataPoint(timestamp)
        datapoint_list.append(dp)
        timestamp = timestamp + binsize

    for item in tempdata:
        try:
            index = bin_indexvalue(item[0])
            data = float(item[1])
            datapoint_list[index].datalist.append(data)
        except IndexError:
            print("Index error in datapoint list")

    binned_data = []
    for item in datapoint_list:
        timevalue = item.timevalue
        if item.avg_data() != null_value:
            datavalue = round(item.max_data() - item.min_data(), 3)
            dp = (timevalue, datavalue)
            binned_data.append(dp)
    return binned_data


def calc_dxdt(bindata):
    templist = []
    for i in range(1, len(bindata)):
        timestamp = bindata[i][0]
        datavalue = bindata[i-1][1] - bindata[i][1]
        dp = (timestamp, datavalue)
        templist.append(dp)
    return templist


def convert_time(tempdata):
    td = []
    for item in tempdata:
        dt = posix2utc(item[0])
        da = item[1]
        dp = (dt, da)
        td.append(dp)
    return td


def db_add_min(data_min):
    db.execute("insert into station_statistics (station_id, data_value, type) values (?,?,?)", [station, data_min, "min"])


def db_get_middle_min():
    result = db.execute("select data_value from station_statistics where station_id = ? and type = ?", [station, "min"])
    query_result = result.fetchall()
    query_result.reverse()
    t = []
    median_result = 1

    if len(query_result) >= 1000:
        for i in range(0, 1000):
            t.append(query_result[i])
        median_result = median(t)
    else:
        if len(query_result) > 2:
            for item in query_result:
                t.append(item[0])
            median_result = median(t)
    print(str(station) + " results, min values: " + str(len(query_result)) + " " + str(median_result))
    return median_result


if __name__ == "__main__":
    # check_create_folders()
    for station in stations:
        current_stationdata = get_data(station)
        tempdata = parse_querydata(current_stationdata)  # a list
        tempdata = filter_median(tempdata)  # a tuple list
        tempdata = bin_data(tempdata)  # a list - one hour bins
        tempdata = convert_time(tempdata)

        s = []
        for item in tempdata:
            s.append(item[1])
        data_min = min(s)
        db_add_min(data_min)
        tempmin = db_get_middle_min()

        t = []
        for item in tempdata:
            dt = item[0]
            dv = item[1]
            scaled_data = round((dv / tempmin), 3)
            dp = (dv, scaled_data)
            t.append(dp)

        # All other calculations are worked on data at 1 minute intervals,
        # incl calculation of K-index, etc.
        nowfile = station + "_1hrdx.csv"
        save_logfiles(nowfile, tempdata)

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
