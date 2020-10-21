import sqlite3
import constants as k
import logging
import time
from datetime import datetime, timedelta
import os
from statistics import mean, median
import matplotlib.pyplot as plt
import math
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
stations = ["GOES_16"]
# stations = k.stations

finish_time = int(time.time())
start_time = finish_time - (60 * 60 * 24)
binsize = 60 * 60
number_bins = int((finish_time - start_time) / binsize)
null_value = ""
half_window = 90

minvalue = 0
maxvalue = 22
null_value = 0
title = "GOES East"
savefile = "spark_goes.png"


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
    db.close()
    return query_result


def posix2utc(posixtime):
    # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


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
            datavalue = round(item.avg_data(), 3)
            dp = (timevalue, datavalue)
            binned_data.append(dp)
    return binned_data


def calc_dxdt(bindata):
    templist = []
    for i in range(1, len(bindata)):
        timestamp = bindata[i][0]
        datavalue = float(bindata[i-1][1]) - float(bindata[i][1])
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

def convert_datetime_to_hour(datetimestring):
    timeformat = "%Y-%m-%d %H:%M:%S"
    # Add one hour to the actual bin time value, so it looks current on the graph.
    # the bin value is correct, this is making the time look current
    dateobject = datetime.strptime(datetimestring, timeformat) + timedelta(hours=1)
    hr = datetime.strftime(dateobject, "%H:%M")
    return hr

def zeroed(tempdata):
    returndata = []
    d = []

    for line in tempdata:
        d.append(line[1])
    minvalue = min(d)

    for line in tempdata:
        datetime = line[0]
        datavalue = line[1] - minvalue
        dp = (datetime, datavalue)
        returndata.append(dp)
    return returndata

if __name__ == "__main__":
    for station in stations:
        current_stationdata = get_data(station)
        db.close()

        tempdata = parse_querydata(current_stationdata)  # a list
        tempdata = filter_median(tempdata)  # a tuple list
        tempdata = bin_data(tempdata)  # a list - one minute bins
        tempdata = calc_dxdt(tempdata)
        tempdata = zeroed(tempdata)
        tempdata = convert_time(tempdata)

        data = []
        hours = []

        for dp in tempdata:
            dd = []
            hr = dp[0]
            da = float(dp[1])
            dd.append(da)
            hr = convert_datetime_to_hour(hr)
            hours.append(hr)
            data.append(dd)
    hours.reverse()

    # print(data)
    # draw the heatmap
    fig, ax = plt.subplots(figsize=(3, 7))
    ax.set_yticks(range(len(hours)))
    ax.set_yticklabels(hours)
    ax.set_xticks([])
    ax.set_ylabel("UTC Hour")
    ax.set_title(title)

    ax.annotate('Now', xy=(0, 0.5), xytext=(0.5, 0.5), color="white")
    ax.annotate('24 hours ago', xy=(0, 23), xytext=(0.5, 23), color="white")

    b = ax.imshow(data, cmap='viridis', interpolation="hanning", vmin=minvalue, vmax=maxvalue,
                  extent=(0, 5, -0.5, 23.5))
    # cbar = ax.figure.colorbar(b, ax=ax)
    # cbar_labels = ['MIN', 'MAX']
    # cbar.set_ticks([minvalue, maxvalue])
    # cbar.set_ticklabels(cbar_labels)

    fig.tight_layout()
    plt.savefig(savefile)
    plt.close('all')
