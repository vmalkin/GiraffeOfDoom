import constants as k
import os.path
import logging
import DataPoint as dp

__author__ = 'Meepo'

# This function is used to build up an array of readings from the diffs file. We might do this if for
# some reason the median filter is not catching spikes, or we have consecutive readings (2 - 5) of spiking.
# The createDiffs function, should have rejected these values.
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


def CreateDiffs(diffsArray):
    try:
        os.remove(k.FILE_4DIFFS)
    except OSError:
        print("WARNING: could not delete " + k.FILE_4DIFFS)
        logging.warning("WARNING: File IO Exception raised - could not delete: " + k.FILE_4DIFFS)

    try:
        with open (k.FILE_4DIFFS,'a') as f:
            f.write("Date/Time (UTC), Ultra-smoothed Differences" + "\n")
            for datapoints in diffsArray:
                f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + "," + str(datapoints.raw_y) + "," + str(datapoints.raw_z) + '\n')
                #f.write(datapoints.dateTime + "," + str(datapoints.raw_x)  + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_4DIFFS)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_4DIFFS)

def Create24(readingsArray):
	# Remove the first segment as it will be not fully averaged
    readingsArray = readingsArray[k.MAG_RUNNINGAVG_COUNT:]

    try:
        os.remove(k.FILE_24HR)
    except OSError:
        print("WARNING: could not delete " + k.FILE_24HR)
        logging.warning("WARNING: File IO Exception raised - could not delete: " + k.FILE_24HR)

    try:
        with open (k.FILE_24HR,'a') as f:
            f.write("Date/Time (UTC), Reading" + "\n")
            for datapoints in readingsArray:
                f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + "," + str(datapoints.raw_y) + "," + str(datapoints.raw_z) + '\n')
                # f.write(datapoints.dateTime + "," + str(datapoints.raw_x)  + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_24HR)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_24HR)

def Create4(readingsArray):
    # get the last 4 hours of data from the array.
    splitvalue = 4 * 60 * k.MAG_READ_FREQ

    fourHrList = readingsArray[(len(readingsArray) - splitvalue):]

    try:
        os.remove(k.FILE_4HR)
    except OSError:
        print("WARNING: could not delete " + k.FILE_4HR)
        logging.warning("WARNING: File IO Exception raised - could not delete: " + k.FILE_24HR)

    try:
        with open (k.FILE_4HR,'a') as f:
            f.write("Date/Time (UTC), Reading" + "\n")
            for datapoints in fourHrList:
                f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + "," + str(datapoints.raw_y) + "," + str(datapoints.raw_z) + '\n')
                # f.write(datapoints.dateTime + "," + str(datapoints.raw_x) + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_4HR)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_24HR)
