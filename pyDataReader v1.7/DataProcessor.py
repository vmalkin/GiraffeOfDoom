import DataPoint
import constants as k
import os.path
import logging
import math
from decimal import Decimal, getcontext
import datafilters
import OutputFileManager as ofm

__author__ = 'vaughn'

# #################################################################################
# Calculate the differences
# #################################################################################
def process_data(input_data_array):
    # If necessary, invert the data so that trends up mean increasing field strength
    data_array = invert_data_array(input_data_array)

    # # ###########################################################################
    # # Initial filter of data: smoothing, remove transients, etc
    # # We're only doing a running average at the moment, but we could add anything,
    # # median filter etc...
    # # This smoothed data is used to create the magnetogram display files.
    # #
    # # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    # #
    # # ###################################### #####################################
    # data_array = datafilters.median_filter_3values(data_array) # Median filter to remove blips
    # smoothed_data_array = datafilters.running_average(data_array) # smooth the array

    # ###########################################################################
    # CReate the differences array and smooth.
    # Do Not Use the smoothed data from previous step. Use original data
    # do several iterations to ensure best appearance.
    # This differences data is used to display rates of change, and minimises the effect
    # of diurnal variation, allowing us to see rapid onsets/changes in the magnetic field.
    # ###########################################################################
    output_diffs = create_diffs_array(data_array)
    for i in range(0,2):
        output_diffs = datafilters.diffs_running_average(output_diffs)

    # # ###########################################################
    # # create the display files for graphing, using ArraySave.CSV
    # #
    # # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    # #
    # # ###########################################################
    # ofm.Create24(smoothed_data_array)
    # ofm.Create4(smoothed_data_array)
    # ofm.CreateDiffs(output_diffs) # use output_diffs data
    # datafilters.binnedaverages(data_array) # use original data

    # ########################################################
    # create the display files for graphing, using Diffs.csv
    # use this if we are having major problems with spikes
    # in final display files
    # ########################################################
    smoothed_data_array = ofm.readings_from_diffs(output_diffs)
    ofm.Create24(smoothed_data_array)
    ofm.Create4(smoothed_data_array)
    ofm.CreateDiffs(output_diffs) # use output_diffs data
    datafilters.binnedaverages(smoothed_data_array) # use original data


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
                dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
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


