import DataPoint
import constants as k
import os.path
import logging
import math
from decimal import Decimal, getcontext
import re
import filemanager_library as ofm

__author__ = 'vaughn'
getcontext().prec = 5

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
    x_value = 0.0
    y_value = 0.0
    z_value = 0.0

    # for each datapoint in the diffs array...
    for datapoints in diffsarray:
        # create cumulative values that will become our "readings"
        x_value = x_value + float(datapoints.raw_x)
        y_value = y_value + float(datapoints.raw_y)
        z_value = z_value + float(datapoints.raw_z)

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
# Calculate the differences
# This function will create an array of differences
# using a wide interval between readings t calculate dh/dt is the same as narrower
# intervals that have to be averaged.
# #################################################################################
def create_diffs_array(readings_array):
    spike_counter = 0
    diffsarray = []
    fivemininterval = k.MAG_READ_FREQ * 10
    counterbit = 0

    if len(readings_array) > 2:
        for i in range (fivemininterval, len(readings_array)):
            counterbit = 0
            diff_x = (Decimal(readings_array[i].raw_x) - Decimal(readings_array[i-fivemininterval].raw_x))
            # Each IF statement checks to see if reading exceeds the spike value. If it does
            # then we change the reading to zero. We trip the counterbit and at the end of the
            # data read incr the spike counter
            if math.sqrt(math.pow(diff_x,2)) > k.NOISE_SPIKE:
                diff_x = 0
                counterbit = 1

            diff_y = (Decimal(readings_array[i].raw_y) - Decimal(readings_array[i-fivemininterval].raw_y))
            if math.sqrt(math.pow(diff_y,2)) > k.NOISE_SPIKE:
                diff_y = 0
                counterbit = 1

            diff_z = (Decimal(readings_array[i].raw_z) - Decimal(readings_array[i-fivemininterval].raw_z))
            if math.sqrt(math.pow(diff_z,2)) > k.NOISE_SPIKE:
                diff_z = 0
                counterbit = 1

            dp = DataPoint.DataPoint(readings_array[i].dateTime,diff_x, diff_y, diff_z)
            diffsarray.append(dp)

            if counterbit == 1:
                spike_counter = spike_counter + 1
                counterbit = 0
    else:
        dp = DataPoint.DataPoint("0000-00-00 00:00:00",0,0,0)
        diffsarray.append(dp)

    return diffsarray


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
def diffs_running_average(input_array):
    getcontext().prec = 5
    displayarray = []
    timeinterval = 4 # minutes

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = int(timeinterval * k.MAG_READ_FREQ)
    AVERAGING_TIME_HALF = int(AVERAGING_TIME / 2)

    # NOW average the cumulative array, smooth out the blips
    if len(input_array) > AVERAGING_TIME:
        for i in range(AVERAGING_TIME_HALF, len(input_array) - AVERAGING_TIME_HALF):
            xvalue = 0
            yvalue = 0
            zvalue = 0

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
# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
#
# we will divide this number evenly so our average represents the midpoint of these
# readings.
# #################################################################################
def running_average(input_array):
    getcontext().prec = 5
    displayarray = []

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = int(k.MAG_RUNNINGAVG_COUNT)
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