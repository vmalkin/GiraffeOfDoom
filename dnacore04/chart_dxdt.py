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


timeformat = '%Y-%m-%d %H:%M:%S'

# Only specific station data makes sense as detrended readings.
stations = ["Ruru_Obs", "GOES_16", "GOES_17", "Geomag_Bz"]
# stations = k.stations

finish_time = int(time.time())
start_time = finish_time - (60 * 60 * 24)
binsize = 60
number_bins = int((finish_time - start_time) / binsize) + 2
null_value = ""
half_window = 90

class Dxdt_datapoint:
    def __init__(self, posixtime, value):
        self.posixtime = posixtime
        self.value = value
        self.last10min_avg = 0

    def posix2utc(self):
        # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        utctime = datetime.datetime.utcfromtimestamp(int(self.posixtime)).strftime(timeformat)
        return utctime

    def printdata(self):
        returnstring = str(self.posix2utc()) + "," + str(self.value) + "," + str(self.last10min_avg)
        return returnstring

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
    dna_core = sqlite3.connect(k.dbfile)
    db = dna_core.cursor()
    result = db.execute("select station_data.posix_time, station_data.data_value from station_data "
                        "where station_data.station_id = ? and station_data.posix_time > ?", [station, start_time])

    query_result = result.fetchall()
    db.close()
    return query_result


def parse_querydata(querydata):
    # turn the readings into rate of change.
    tempdata = []
    for i in range(1, len(querydata)):
        date = querydata[i][0]
        newdata = querydata[i][1]
        dp = (date, newdata)
        tempdata.append(dp)
    return tempdata


def save_logfiles(filename, datalist):
    with open(filename, "w") as n:
        for item in datalist:
            n.write(item.printdata() + "\n")
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
            datavalue = round(item.avg_data(), 3)
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


def avg_last10mins(tuplelist):
    returnlist = []
    for i in range(9, len(tuplelist)):
        timevalue = tuplelist[i][0]
        currentdata = tuplelist[i][1]
        temp = []
        for j in range(0, 9):
            temp.append(tuplelist[i-j][1])
        meandata = mean(temp)
        dp = Dxdt_datapoint(timevalue, currentdata)
        dp.last10min_avg = meandata
        returnlist.append(dp)
    return returnlist




if __name__ == "__main__":
    # check_create_folders()
    for station in stations:
        current_stationdata = get_data(station)
        tempdata = parse_querydata(current_stationdata)  # a list
        tempdata = filter_median(tempdata)  # a tuple list
        tempdata = bin_data(tempdata)  # a list - one minute bins
        tempdata = calc_dxdt(tempdata)  # a tuple list
        tempdata = avg_last10mins(tempdata)

        # All other calculations are worked on data at 1 minute intervals,
        # incl calculation of K-index, etc.

        nowfile = station + "_dxdt.csv"
        save_logfiles(nowfile, tempdata)

    print("Closing database and exiting")

