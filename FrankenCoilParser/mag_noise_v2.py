import re
import time
import calendar
import datetime
import pickle
from statistics import mean, median, stdev
import os

datafile = "broad_noise.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"


class DataPoint:
    def __init__(self, utc_time, data, median_value = 0, stdev_value = 0 ):
        self.utc_time = utc_time
        self.data = data
        self.median_value = round(median_value,4)
        self.stdev_value = round(stdev_value,4)

    def utc_to_posix(self):
        date_obj = datetime.datetime.strptime(self.utc_time, dt_format)
        posixtime = calendar.timegm(date_obj.timetuple())
        return posixtime

    def print_header(self):
        return "DateTime UTC, -2*sigma, -1*sigma, Mean, 1*sigma, 2*sigma, Frequency (Hz)"

    def print_values(self):
        sigma_1neg = round((self.median_value - self.stdev_value),4)
        sigma_2neg = round((self.median_value - (2 * self.stdev_value)),4)
        sigma_1 = round((self.median_value + self.stdev_value),4)
        sigma_2 = round((self.median_value + (2 * self.stdev_value)),4)

        returnstring = self.utc_time + "," + str(sigma_2neg) + "," + str(sigma_1neg) + "," + str(self.median_value) + "," + str(sigma_1) + "," + str(sigma_2) + "," + str(self.data)
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
    datalist = []
    temp_reading = []
    mean_list = []
    stdev_list = []

    if os.path.isfile("mean_list.pkl"):
        mean_list = pickle.load(open("mean_list.pkl", "rb"))
        print("List is " + str(len(mean_list)) + " records long")

    if os.path.isfile("stdev_list.pkl"):
        stdev_list = pickle.load(open("stdev_list.pkl", "rb"))
        print("List is " + str(len(stdev_list)) + " records long")

    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line = line.split(",")
            dp = DataPoint(line[0], line[1].strip())
            if re.match(regex, line[0]):
                datalist.append(dp)
                temp_reading.append(float(line[1].strip()))

    # calc median, std dev.
    # append med, stddev to lists. Calc median values of each
    mean_list.append(mean(temp_reading))
    stdev_list.append(stdev(temp_reading))
    print("Appended new stats values")

    mean_value = median(mean_list)
    stdev_value = median(stdev_list)

    # parse out the data for the current 24 hours
    returnlist = []
    endtime = time.time()
    starttime = endtime - 86400

    for dp in datalist:
        if dp.utc_to_posix() > starttime:
            returnlist.append(dp)

    # median filter of data
    returnlist = filter_median(returnlist)
    print("Median filter...")

    # one minute bins
    returnlist = filter_binner(returnlist)
    print("Binning values...")

    # add median and +/- 1xSD and 2xSD values
    finished_data = []
    for dp in returnlist:
        dp2 = DataPoint(dp.utc_time, dp.data, mean_value, stdev_value)
        finished_data.append(dp2)

    # create the display file for upload to DunedinAurora.NZ
    with open("mag_noise.csv", "w") as g:
        g.write(finished_data[0].print_header() + "\n")

        for dp in finished_data:
            g.write(dp.print_values() + "\n")
    g.close()
    print("Data files created")

    pickle.dump(mean_list, open("mean_list.pkl", "wb"),0)
    pickle.dump(stdev_list, open("stdev_list.pkl", "wb"),0)
    print(mean_list)
    print(stdev_list)
    print("Stats data saved - FINISHED")
