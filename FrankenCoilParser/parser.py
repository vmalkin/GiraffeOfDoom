"""
Generic parser for Spectrum Lab save files.
Customised for Wideband Magnetic Riometer

Data file lines have the format of:
UTCdatetime, data_a, data_b, data_c, etc...
"""
import time
from statistics import median
from datetime import datetime
from calendar import timegm
import numpy as np
import re


datafile = "hiss.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
stationname = "dna_hiss"
graphing_file = stationname + "_graph.csv"
median_window = 1  # Full window = halfwindow * 2 + 1

def filter_median(item_list):
    """
    Takes in a list of DataPoints and performs a median filter on the list. The list is truncated at the start
    and end by one halfwindow
    """
    returnlist = []

    for i in range(median_window, len(item_list) - median_window):
        data_store = []
        for j in range(0 - median_window, median_window + 1):
            d = float(item_list[i + j])
            data_store.append(d)
        medianvalue = median(data_store)
        returnlist.append(medianvalue)
    return returnlist


def utc_to_posix(utc_time):
    date_obj = datetime.strptime(utc_time, dt_format)
    posixtime = timegm(date_obj.timetuple())
    return posixtime


def open_file(datafile):
    starttime = time.time() - 86400
    returnlist = []
    with open(datafile, "r") as c:
        for line in c:
            line = line.strip("\n")
            line = line.split(",")
            datething = line[0]
            if re.match(regex, datething):
                if utc_to_posix(datething) > starttime:
                    returnlist.append(line)
    return returnlist


def filter_nulls(data):
    null = None
    returnlist = []
    for item in data:
        if item == 0:
            returnlist.append(null)
        elif item > 500:
            returnlist.append(null)
        else:
            returnlist.append(item)
    return returnlist


if __name__ == "__main__":
    data_last_24_hours = open_file(datafile)
    npdata = np.array(data_last_24_hours)
    rowlen = npdata.shape[1]

    # Slice the array into separate lists for each column
    master_data = []
    datetimes = npdata[:, 0]
    for i in range(1, rowlen):
        master_data.append(npdata[:, i])


    # Perform whatever functions to the lists
    filtered = []
    for data in master_data:
        filtered.append(filter_median(data))

    # FINALLY Remove extreme values and replace with a null
    nulled = []
    for data in filtered:
        nulled.append(filter_nulls(data))

    # Reconstitute the lists into a single file for display
    # AFter the filtering processes, the length of data will differ from the original
    # data. Start iterating from the correct record in datetime to compensate
    difference = len(datetimes) - len(nulled[0])
    startindex = difference / 2







