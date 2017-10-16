import DataPoint
import constants as k
import os.path
import logging
import math
from decimal import Decimal, getcontext
import re
import filemanager_library as ofm

__author__ = 'vaughn'
getcontext().prec = 10

# #################################################################################
# Data processing script
# this library is for anything that crunches and manipulates data
#
# #################################################################################

# #################################################################################
# This function is used to build up an array of readings from the diffs file. We might do this if for
# some reason the median filter is not catching spikes, or we have consecutive readings (2 - 5) of spiking.
# The createDiffs function, should have rejected these values.
# #################################################################################
def readings_from_diffs(diffsarray):
    # set up the return array and x,y, and z storage values
    outputarray = []
    x_value = float(0.0)
    y_value = float(0.0)
    z_value = float(0.0)

    # for each datapoint in the diffs array...
    for datapoints in diffsarray:
        # create cumulative values that will become our "readings"
        x_value = x_value * float(datapoints.raw_x)
        y_value = y_value * float(datapoints.raw_y)
        z_value = z_value * float(datapoints.raw_z)

        # create a datapoint with the new values. Append to return array
        appenddata = DataPoint.DataPoint(datapoints.dateTime, x_value, y_value, z_value)
        outputarray.append(appenddata)

    # return array
    return outputarray

# #################################################################################
# data inverter
# If necessary, invert the data so that trends up mean increasing field strength
# #################################################################################
def invert_data_array(data_array):
    returnarray = []
    for i in range(0, len(data_array)):
        x = Decimal(data_array[i].raw_x) * k.FIELD_CORRECTION
        y = Decimal(data_array[i].raw_y) * k.FIELD_CORRECTION
        z = Decimal(data_array[i].raw_z) * k.FIELD_CORRECTION
        dp = DataPoint.DataPoint(data_array[i].dateTime, x, y, z)
        returnarray.append(dp)

    return returnarray


# #################################################################################
# Datafilters
# THis script may just be merged into the dataprocessor script
#
# #################################################################################

# #################################################################################
# Median filter based on 3 values
#
# #################################################################################
def median_filter_3values(arraydata):
    outputarray = []

    for i in range(1,len(arraydata)-1):
        xlist = []
        ylist = []
        zlist = []

        for j in range(-1,2):    # -1, 0, 1
            k = i + j
            xlist.append(arraydata[k].raw_x)
            ylist.append(arraydata[k].raw_y)
            zlist.append(arraydata[k].raw_z)

        xlist.sort()
        ylist.sort()
        zlist.sort()

        dp = DataPoint.DataPoint(arraydata[i].dateTime, xlist[1],ylist[1], zlist[1])

        outputarray.append(dp)

    return outputarray


# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
#
# we will divide this number evenly so our average represents the midpoint of these
# readings.
# #################################################################################
def running_average(input_array, averaging_interval):
    getcontext().prec = 10
    displayarray = []

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = int(averaging_interval)
    AVERAGING_TIME_HALF = int(AVERAGING_TIME / 2)

    # NOW average the cumulative array, smooth out the blips
    if len(input_array) > AVERAGING_TIME:
        for i in range(AVERAGING_TIME_HALF, len(input_array) - AVERAGING_TIME_HALF):
            xvalue = Decimal(0)
            yvalue = Decimal(0)
            zvalue = Decimal(0)

            # This is where we average for the time i before and after i.
            for j in range(0, AVERAGING_TIME):
                xvalue = xvalue + Decimal(input_array[(i - AVERAGING_TIME_HALF) + j].raw_x)
                yvalue = yvalue + Decimal(input_array[(i - AVERAGING_TIME_HALF) + j].raw_y)
                zvalue = zvalue + Decimal(input_array[(i - AVERAGING_TIME_HALF) + j].raw_z)

            xvalue = Decimal(xvalue / AVERAGING_TIME)
            yvalue = Decimal(yvalue / AVERAGING_TIME)
            zvalue = Decimal(zvalue / AVERAGING_TIME)

            displaypoint = DataPoint.DataPoint(input_array[i].dateTime, xvalue, yvalue, zvalue)
            displayarray.append(displaypoint)

    else:
        displayarray = input_array

    return displayarray