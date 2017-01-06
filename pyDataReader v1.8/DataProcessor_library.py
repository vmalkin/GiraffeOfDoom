import DataPoint
import constants as k
import os.path
import logging
import math
from decimal import Decimal, getcontext
import datafilters_library
import filemanager_library as ofm

__author__ = 'vaughn'

# #################################################################################
# Data processing script
# this script is for anything that crunches and manipulates data
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
        appenddata = dp.DataPoint(datapoints.dateTime, x_value, y_value, z_value)
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
# #################################################################################
def create_diffs_array(readings_array):
    diffsarray = []
    if len(readings_array) > 2:
        for i in range (1, len(readings_array)):
            # here we deal with flipping. differences should be in the order of 10s. It we're seeing 100s, there's an issue.
            # DIRECTLY set up the difference values for the main reading array datapoints. This is stored to the raw logfiles
            # APPLY field correction - increasing readings should be increasing field strength
            diff_x = (Decimal(readings_array[i].raw_x) - Decimal(readings_array[i-1].raw_x))
            if math.sqrt(math.pow(diff_x,2)) > k.MAG3110_FLIP:
                diff_x = 0

            diff_y = (Decimal(readings_array[i].raw_y) - Decimal(readings_array[i-1].raw_y))
            if math.sqrt(math.pow(diff_y,2)) > k.MAG3110_FLIP:
                diff_y = 0

            diff_z = (Decimal(readings_array[i].raw_z) - Decimal(readings_array[i-1].raw_z))
            if math.sqrt(math.pow(diff_z,2)) > k.MAG3110_FLIP:
                diff_z = 0

            dp = DataPoint.DataPoint(readings_array[i].dateTime,diff_x, diff_y, diff_z)
            diffsarray.append(dp)
    else:
        dp = DataPoint.DataPoint("0000-00-00 00:00:00",0,0,0)
        diffsarray.append(dp)

    return diffsarray




