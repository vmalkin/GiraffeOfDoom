import DataPoint
import constants as k
import os.path
import logging

__author__ = 'Meepo'

def Create24(readingsArray):
    try:
        os.remove(k.FILE_24HR)
    except OSError:
        print("WARNING: could not delete " + k.FILE_24HR)
        logging.warning("WARNING: File IO Exception raised - could not delete: " + k.FILE_24HR)

    try:
        with open (k.FILE_24HR,'a') as f:
            f.write("Date/Time (NZ), Reading" + "\n")
            for datapoints in readingsArray:
                # f.write(datapoints.dateTime + "," + str(datapoints.rawMagX) + "," + str(datapoints.rawMagY) + "," + str(datapoints.rawMagZ) + '\n')
                f.write(datapoints.dateTime + "," + str(datapoints.rawMagX)  + '\n')
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
            f.write("Date/Time (NZ), Reading" + "\n")
            for datapoints in fourHrList:
                # f.write(datapoints.dateTime + "," + str(datapoints.rawMagX) + "," + str(datapoints.rawMagY) + "," + str(datapoints.rawMagZ) + '\n')
                f.write(datapoints.dateTime + "," + str(datapoints.rawMagX) + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_4HR)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_24HR)
