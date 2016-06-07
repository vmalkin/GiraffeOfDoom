import constants as k
import os.path
import logging

__author__ = 'Meepo'



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
