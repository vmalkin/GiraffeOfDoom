import DataPoint
import constants as k
import os.path
import logging
import OutputFileManager as ofm
import math
from decimal import Decimal, getcontext

__author__ = 'vaughn'

# #################################################################################
# Calculate the differences
# #################################################################################
def process_data(data_array):
    # calculate the diffs, average and write out
    output_diffs = create_diffs(data_array)
    output_diffs = ultra_smooth_array(output_diffs)#  Put thru twice to really flatten out
    output_diffs = ultra_smooth_array(output_diffs)#  Put thru twice to really flatten out
    # write out to file
    ofm.CreateDiffs(output_diffs)

    # create the cumulative array, average and write out
    output_cumulatives = create_cumulative(data_array)
    output_cumulatives = smooth_array(output_cumulatives)

    # write out to file
    ofm.Create24(output_cumulatives)
    ofm.Create4(output_cumulatives)

    SaveRawArray(data_array)        # Save the array to the ArraySave.csv file loaded at the beginning

    if len(output_cumulatives) > 0:
        print(output_cumulatives[len(output_cumulatives) - 1].dateTime + " " +
              str(output_cumulatives[len(output_cumulatives) - 1].raw_x))


# #################################################################################
# Calculate the differences
# This function takes in the array of datapoints that have actual values and
# returns a new array that consists of timestamp and the differences between datapoints
# #################################################################################
def create_diffs(readings_array):
    for i in range (1, len(readings_array)):
        # here we deal with flipping. differences should be in the order of 10s. It we're seeing 100s, there's an issue.
        # DIRECTLY set up the difference values for the main reading array datapoints. This is stored to the raw logfiles
        # APPLY field correction - incresing readings should be increasing field strength
        readings_array[i].raw_diff_x = (Decimal(readings_array[i].raw_x) - Decimal(readings_array[i-1].raw_x)) * k.FIELD_CORRECTION
        if math.sqrt(math.pow(readings_array[i].raw_diff_x,2)) > k.MAG3110_FLIP:
            readings_array[i].raw_diff_x = 0

        readings_array[i].raw_diff_y = (Decimal(readings_array[i].raw_y) - Decimal(readings_array[i-1].raw_y)) * k.FIELD_CORRECTION
        if math.sqrt(math.pow(readings_array[i].raw_diff_y,2)) > k.MAG3110_FLIP:
            readings_array[i].raw_diff_y = 0

        readings_array[i].raw_diff_z = (Decimal(readings_array[i].raw_z) - Decimal(readings_array[i-1].raw_z)) * k.FIELD_CORRECTION
        if math.sqrt(math.pow(readings_array[i].raw_diff_z,2)) > k.MAG3110_FLIP:
            readings_array[i].raw_diff_z = 0

    outputdiffs = []

    for i in range(1,len(readings_array)):
        datetime = readings_array[i].dateTime
        plotX = Decimal(readings_array[i].raw_diff_x)
        plotY = Decimal(readings_array[i].raw_diff_y)
        plotZ = Decimal(readings_array[i].raw_diff_z)

        plotpoint = DataPoint.DataPoint(datetime, plotX, plotY, plotZ)
        outputdiffs.append(plotpoint)

    # Return an array out Differences
    return outputdiffs


# #################################################################################
# Create the cumulative data array and write out the files for plotting.
# This function takes in the array of differences and returns a new array of
# datapoints with new absolute values that are corrected for any flipping or
# errors from the hardware.
# #################################################################################
def create_cumulative(input_array):

    # Now convert the array from difference to a cumulative sum. This is what will be plotted.
    cumulativeArray = []
    plot_x = 0
    plot_y = 0
    plot_z = 0

    for i in range(1,len(input_array)):
        datetime = input_array[i].dateTime
        plot_x = Decimal(input_array[i - 1].raw_diff_x) + plot_x
        plot_y = Decimal(input_array[i - 1].raw_diff_y) + plot_y
        plot_z = Decimal(input_array[i - 1].raw_diff_z) + plot_z

        plotpoint = DataPoint.DataPoint(datetime, plot_x, plot_y, plot_z)

        cumulativeArray.append(plotpoint)

    return cumulativeArray


# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# #################################################################################
def ultra_smooth_array(imput_array):
    getcontext().prec = 3
    MAG_RUNNINGAVG_COUNT = 40

    # NOW average the cumulative array, smooth out the blips
    if len(imput_array) > MAG_RUNNINGAVG_COUNT:

        displayarray = []

        for i in range(len(imput_array)-1, MAG_RUNNINGAVG_COUNT, -1):
            xvalue = 0
            yvalue = 0
            zvalue = 0

            for j in range(0, MAG_RUNNINGAVG_COUNT):
                xvalue = xvalue + imput_array[i-j].raw_x
                yvalue = yvalue + imput_array[i-j].raw_y
                zvalue = zvalue + imput_array[i-j].raw_z

            xvalue = Decimal(xvalue / MAG_RUNNINGAVG_COUNT)
            yvalue = Decimal(yvalue / MAG_RUNNINGAVG_COUNT)
            zvalue = Decimal(zvalue / MAG_RUNNINGAVG_COUNT)

            displaypoint = DataPoint.DataPoint(imput_array[i].dateTime, xvalue, yvalue, zvalue)
            displayarray.append(displaypoint)

        displayarray.reverse()
    else:
        displayarray = imput_array

    return displayarray


# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# #################################################################################
def smooth_array(imput_array):
    getcontext().prec = 3
    # NOW average the cumulative array, smooth out the blips
    if len(imput_array) > k.MAG_RUNNINGAVG_COUNT:

        displayarray = []

        for i in range(len(imput_array)-1, k.MAG_RUNNINGAVG_COUNT, -1):
            xvalue = 0
            yvalue = 0
            zvalue = 0

            for j in range(0, k.MAG_RUNNINGAVG_COUNT):
                xvalue = xvalue + imput_array[i-j].raw_x
                yvalue = yvalue + imput_array[i-j].raw_y
                zvalue = zvalue + imput_array[i-j].raw_z

            xvalue = Decimal(xvalue / k.MAG_RUNNINGAVG_COUNT)
            yvalue = Decimal(yvalue / k.MAG_RUNNINGAVG_COUNT)
            zvalue = Decimal(zvalue / k.MAG_RUNNINGAVG_COUNT)

            displaypoint = DataPoint.DataPoint(imput_array[i].dateTime, xvalue, yvalue, zvalue)
            displayarray.append(displaypoint)

        displayarray.reverse()
    else:
        displayarray = imput_array

    return displayarray


# #################################################################################
# Create the raw datapoint array from the save file
# #################################################################################
def CreateRawArray(readings):
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(k.FILE_ROLLING):
        with open(k.FILE_ROLLING) as e:
            for line in e:
                line = line.strip() # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                # See the datapoint object/constructor for the current values it holds.
                dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3],
                                         values[4], values[5], values[6])
                readings.append(dp)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded. Using new array.")

# #################################################################################
# Save the raw datapoint array to the save file
# #################################################################################
def SaveRawArray(readings):
    # export array to array-save file
        try:
            with open (k.FILE_ROLLING, 'w') as w:
                for dataObjects in readings:
                    w.write(dataObjects.print_values() + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + k.FILE_ROLLING)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_ROLLING)

# #################################################################################
#  Append a new datapoint
# #################################################################################
def AppendDataPoint(datapoint, readingsArray):
    # Append the datapoint to the array. Prune off the old datapoint if the array is 24hr long
    if(len(readingsArray) < k.MAG_READ_FREQ * 60 * 24):
        readingsArray.append(datapoint)
    else:
        readingsArray.pop(0)
        readingsArray.append(datapoint)
