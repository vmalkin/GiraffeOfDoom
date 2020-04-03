import re
import time
import calendar
import datetime
from statistics import mean, median


datafile = "broad_noise.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
datalist = []


class DataPoint:
    def __init__(self, utc_time, data):
        self.utc_time = utc_time
        self.data = data

    def utc_to_posix(self):
        date_obj = datetime.datetime.strptime(self.utc_time, dt_format)
        posixtime = calendar.timegm(date_obj.timetuple())
        return posixtime

    def print_header(self):
        return "DateTime UTC, Frequency (Hz))"

    def print_values(self):
        returnstring = str(self.utc_time) + "," + str(self.data)
        return returnstring


def filter_median(object_list):
    """Takes in a list of DataPoints and performs a median filter on the object's datavalue"""
    filterwindow = 150
    returnlist = []

    for i in range(filterwindow, len(object_list) - 1):
        data_store = []
        time = object_list[i].utc_time

        for j in range(0, filterwindow - 1):
            k = i - j
            data = object_list[k].data
            data_store.append(data)

        if len(data_store) > 0:
            data = median(data_store)
            dp = DataPoint(time, data)
            returnlist.append(dp)

    return returnlist


def filter_binner(object_list):
    """Takes in a list of DataPoints and bins the data"""
    filterwindow = 30
    returnlist = []

    for i in range(filterwindow, len(object_list) - 1, filterwindow):
        data_store = []
        time = object_list[i].utc_time

        for j in range(0, filterwindow - 1):
            k = i - j
            data = float(object_list[k].data)
            data_store.append(data)

        if len(data_store) > 0:
            data = round(mean(data_store), 3)
            dp = DataPoint(time, data)
            returnlist.append(dp)

    return returnlist


if __name__ == "__main__":
    # open master csv data, load into array
    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line = line.split(",")
            dp = DataPoint(line[0], line[1].strip())
            if re.match(regex, line[0]):
                datalist.append(dp)

    # parse out the data for the current 24 hours
    returnlist = []
    endtime = time.time()
    starttime = endtime - 86400

    for dp in datalist:
        if dp.utc_to_posix() > starttime:
            returnlist.append(dp)

    # median filter
    returnlist = filter_median(returnlist)

    # one minute bins
    returnlist = filter_binner(returnlist)

    # create the display file for upload to DunedinAurora.NZ
    with open("mag_noise.csv", "w") as g:
        g.write(returnlist[0].print_header() + "\n")

        for dp in returnlist:
            g.write(dp.print_values() + "\n")
    g.close()
