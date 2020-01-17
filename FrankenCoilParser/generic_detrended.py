"""
Generic parser for Spectrum Lab save files.
provides detrended values with standard deviation bars
"""
import re
import time
import calendar
import datetime
from statistics import mean, median, stdev
import pickle
import os


datafile = "1mins_Ruru_Rapidrun.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
stationname = "dna_noise"
graphing_file = stationname + "_graphing.csv"
stdev_file = stationname + "_stdev.pkl"


class DataPoint:
    def __init__(self, utc_time, data, average_value=0, median_value=0, stdev_value=0):
        self.utc_time = utc_time
        self.data = data
        self.average_value = float(average_value)
        self.median_value = float(median_value)
        self.stdev_value = float(stdev_value)

    def utc_to_posix(self):
        date_obj = datetime.datetime.strptime(self.utc_time, dt_format)
        posixtime = calendar.timegm(date_obj.timetuple())
        return posixtime

    def print_header(self):
        # return "DateTime UTC, 3hr Average, Data"
        return "DateTime UTC, -2*SD, -1*SD, 1*SD, 2*SD, Detrended Data"

    def print_diffs(self):
        diff_value = self.data - self.average_value
        diff_value = round(diff_value, 4)
        return diff_value

    def print_values(self):
        sigma_1neg = round((self.median_value - self.stdev_value),4)
        sigma_2neg = round((self.median_value - (2 * self.stdev_value)),4)
        sigma_1 = round((self.median_value + self.stdev_value),4)
        sigma_2 = round((self.median_value + (2 * self.stdev_value)),4)

        returnstring = self.utc_time + "," + str(sigma_2neg) + "," + str(sigma_1neg) + "," +  str(sigma_1) + "," + str(sigma_2) + "," + str(self.print_diffs())
        return returnstring


def filter_median(object_list):
    """Takes in a list of DataPoints and performs a median filter on the object's datavalue"""
    filterwindow = 3
    returnlist = []

    for i in range(filterwindow, len(object_list) - 1):
        data_store = []
        time = object_list[i].utc_time
        average_value = object_list[i].average_value

        for j in range(0, filterwindow - 1):
            k = i - j
            data = float(object_list[k].data)
            data_store.append(data)

        if len(data_store) > 0:
            data = median(data_store)
            dp = DataPoint(time, data, average_value)
            returnlist.append(dp)

    return returnlist


def filter_average(object_list):
    returnlist = []
    half_window = 30

    for i in range(half_window, len(object_list) - half_window):
        templist = []
        datetime = object_list[i].utc_time
        data = object_list[i].data

        for j in range(-1 * half_window, half_window):
            d = float(object_list[i+j].data)
            templist.append(d)

        avg_data = mean(templist)
        dp = DataPoint(datetime, data, avg_data)
        returnlist.append(dp)
    return returnlist


if __name__ == "__main__":
    # open master csv data, load into array
    datalist = []

    # ***********************************************************************************
    # for master lists with several columns, parse out the data column, ignore the others
    # ***********************************************************************************
    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line = line.split(",")
            datething = line[0]
            datathing = line[1].strip()  # Change this as needed
            dp = DataPoint(datething, datathing)

            if re.match(regex, datething):
                datalist.append(dp)

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

    returnlist = filter_average(returnlist)
    print("Smoothing data...")

    # ***********************************************************************************
    # Calculate the standard deviations
    # ***********************************************************************************
    temp_reading = []
    for d in returnlist:
        temp_reading.append(d.print_diffs())

    stdev_list = []

    if os.path.isfile(stdev_file):
        stdev_list = pickle.load(open(stdev_file, "rb"))
        print("List is " + str(len(stdev_list)) + " records long")

    # calc std dev.
    stdev_list.append(stdev(temp_reading))
    print("Appended new stats values")
    stdev_value = round(median(stdev_list), 4)

    # # prune the lists if too long
    if len(stdev_list) >= 5000:
        stdev_list = []
        stdev_list.append(stdev_value)

    # add median and +/- 1xSD and 2xSD values
    for dp in returnlist:
        dp.stdev_value = stdev_value

    finished_data = returnlist
    # create the display file for upload to DunedinAurora.NZ
    with open(graphing_file, "w") as g:
        g.write(finished_data[0].print_header() + "\n")

        for dp in finished_data:
            g.write(dp.print_values() + "\n")
    g.close()

    print("Data files created")
    # pickle.dump(mean_list, open("mean_list.pkl", "wb"),0)
    pickle.dump(stdev_list, open(stdev_file, "wb"),0)
    # print(mean_list)
    print(stdev_list)
    print("Stats data saved - FINISHED")
