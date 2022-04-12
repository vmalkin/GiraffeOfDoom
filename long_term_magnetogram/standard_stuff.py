"""
This file contains any global constants as well as standard methods that I use all the time.
"""
import datetime
from statistics import mean

# Default or global values or constants
file_list = "files.txt"
sightings_list = "sightings.txt"
detrender_half_window = 10

# ##############################################################################
# general utility methods
def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

# ##############################################################################
# A simple detrender that computes a running average across the bulk of data and a simple
# linear detrend at the ends of the data.
def calc_start(datalist):
    returnlist = []
    data_start = float(datalist[0])
    data_end = float(datalist[detrender_half_window - 1])
    rate = (data_end - data_start) / detrender_half_window
    d = data_start
    returnlist.append(data_start)

    for i in range(0, detrender_half_window - 1):
        d = d + rate
        returnlist.append(round(d,3))
        # print(i, datalist[i], returnlist[i])
    return returnlist


def calc_end(datalist):
    returnlist = []
    data_start = float(datalist[len(datalist) - detrender_half_window])
    data_end = float(datalist[len(datalist) - 1])
    rate = (data_end - data_start) / detrender_half_window
    d = data_start
    returnlist.append(data_start)

    for i in range(len(datalist) - detrender_half_window, len(datalist) - 1):
        d = d + rate
        returnlist.append(round(d,3))
    return returnlist

def calc_middle(datalist):
    returnlist = []

    for i in range(detrender_half_window, len(datalist) - detrender_half_window):
        t = []
        for j in range(0 - detrender_half_window, detrender_half_window):
            t.append(float(datalist[i + j]))

        if len(t) > 0:
            d = mean(t)
        else:
            d = 0
        returnlist.append(round(d,3))

    return returnlist
# ##############################################################################