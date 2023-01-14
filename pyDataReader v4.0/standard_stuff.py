"""
This file contains any global constants as well as standard methods that I use all the time.
"""
import datetime
import time
from statistics import mean, median
from calendar import timegm

# Default or global values or constants
file_list = "files.txt"
sightings_list = "sightings.txt"
cme_list = "cme.csv"
detrender_half_window = 10

# ##############################################################################
# general utility methods
def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


def filter_median(numerical_data, filter_halfwindow):
    # Takes in an array of csv data. single values only.
    returnarray = []
    if len(numerical_data) > 2 * filter_halfwindow + 1:
        for i in range(filter_halfwindow, len(numerical_data) - filter_halfwindow):
            t = []
            for j in range(-filter_halfwindow, filter_halfwindow):
                t.append(numerical_data[i + j])
            v = mean(t)
            returnarray.append(v)
    else:
        returnarray = numerical_data
    return returnarray


def filter_mean(numerical_data, filter_halfwindow):
    # Takes in an array of csv data. single values only.
    returnarray = []
    t = []
    for i in range(0, len(numerical_data)):
        t.append(numerical_data[i])
        if len(t) >= 2 * filter_halfwindow:
            t.pop(0)
            v = median(t)
            returnarray.append(v)
    else:
        returnarray = numerical_data
    return returnarray

