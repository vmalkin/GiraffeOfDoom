import os.path
import logging
import constants as k
import math
from decimal import Decimal, getcontext
from datetime import datetime
import time


class DhdtData():
    def __init__(self, posix_date, data_value):
        self.posix_date = posix_date
        self.data_value = data_value

# #################################################################################
# Calculate the differences
# This function will create an array of differences based on data of the format
# [posix_date, data_value]
# No smoothing has been applied to this.
# Blips over a threshold value WILL be zeroed
# #################################################################################
def create_diffs_array(readings_array):
    diffsarray = []

    for i in range(1, len(readings_array)):
        timestamp_value = readings_array[i].posix_time

        # calculate the rate of change (dH/dt)
        data_value = readings_array[i].data_1 - readings_array[i-1].data_1

        # If the data value is over the noise threshold, then we'll reset it to zero
        if data_value > k.noise_spike:
            data_value = 0

        dp = DhdtData(timestamp_value, data_value)

    return diffsarray

# #################################################################################
# Calculate the differences
# This function will create an array of differences
# #################################################################################
def rebuild_originaldata(diffsdata, startvalue):
    pass


# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
# Data format is the DhdtData class in this file.
# #################################################################################
def running_average(input_array, averaging_interval):
    displayarray = []

    while len(input_array) > averaging_interval:
        for i in range(averaging_interval + 1, len(input_array)):
            datavalue = 0
            datetime = input_array[i].posix_date

            for j in range(0, averaging_interval):
                newdata = input_array[i-j].data_value
                datavalue = datavalue + newdata

            datavalue = round((datavalue / averaging_interval), 3)
            appendvalue = DhdtData(datetime, datavalue)
            displayarray.append(appendvalue)

    return displayarray


# #################################################################################
# calculate the lines that will be displayed as background threshold bars
# these will be appended to the diffs data before being finally saved.
# The data is saved out to a CSV with the format [UTC_time, accrued_min_values, count_of_averages]
# #################################################################################
def calculate_minmax_values(diffs_data):
    r1 = []  # the min/max/dhdt data
    r2 = []  # reorganised r1 that is retured
    r3 = []  # short values - 1 hr summary

    BACKGROUND_VALUE = 0.02  # empirically derived background during geomag quiet conditions.


    hour_interval = k.MAG_READ_FREQ * 60

    if len(diffs_data) > hour_interval:
        # reverse the array. this ensures that our bin starts from now and goes back
        diffs_data.reverse()
        # Assuming the array represents contiguous values. We count out blocks of one hour. For each hour
        # we calculate the min/max value.
        for i in range(0, len(diffs_data) - hour_interval, hour_interval):
            min = 10000
            max = -10000

            # find the min max value for the hour
            for j in range(0, hour_interval):
                datasplit = diffs_data[i+j].split(",")
                datevalue = datasplit[0]
                datavalue = datasplit[1]

                if float(datavalue) < float(min):
                    min = datavalue
                if float(datavalue) > float(max):
                    max = datavalue

            # append the min and max values to the data. Write out to the
            # display file
            for j in range(0, hour_interval):
                datavalue = diffs_data[i+j] + "," + min + "," + max
                r1.append(datavalue)

        # reorganise the data for display in Highcharts
        for i in range(0, len(r1)):
            datasplit = r1[i].split(",")
            date = datasplit[0]
            reading = datasplit[1]
            min = datasplit[2]
            max = datasplit[3]

            newreading  = date + "," + min + "," + max + "," + reading
            r2.append(newreading)

        # create the array of short values modding on the hour interval
        for i in range(0, len(r2), hour_interval):
            datasplit = r2[i].split(",")
            date = datasplit[0]
            maxvalue = datasplit[2]
            minvalue = datasplit[1]

            localindex = float(maxvalue) - float(minvalue)

            # make local index the ratio of the current reading to the usual background.
            try:
                localindex = float(localindex / BACKGROUND_VALUE)
            except ZeroDivisionError:
                localindex = 0

            r3_data = date + "," + str(localindex)
            r3.append(r3_data)

        # finally revert the data
    else:
        r2 = diffs_data

    # save the short values to file and return the diffs data
    r3.reverse()
    savevalues("publish/shortdiffs.csv", r3)
    r2.reverse()
    return r2


# #################################################################################
# load an array from file
# #################################################################################
def loadvalues(filename, array_name):
    readings = []
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(k.FILE_ROLLING):
        with open(k.FILE_ROLLING) as e:
            for line in e:
                line = line.strip()  # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                # See the datapoint object/constructor for the current values it holds.
                # dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
                readings.append(values)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded. Using new array.")

    return readings


# #################################################################################
# save an array to file
# #################################################################################
def savevalues(filename, array_name):
    # export array to array-save file
        try:
            with open(filename, 'w') as w:
                for dataObjects in array_name:
                    w.write(dataObjects + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + filename)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + filename)


# #################################################################################
# Wrapper function to process diffs
# #################################################################################
def process_differences(data_array):
    # For a start, the data array has to be at least two readings big
    while len(data_array) > 2:
        # create the array of dF/dt
        diffs_data = create_diffs_array(data_array)

        # recalculate and save a corrected display file free from blips
        startvalue = data_array[0].data_1
        rebuilt_data = rebuild_originaldata(diffs_data, startvalue)
        savevalues("display.rebuiltdata.csv", rebuilt_data)

        # smooth the diffs to show the trend. Two passes at 5 minutes is usually ok.
        window = k.mag_read_freq * 5
        diffs_data = running_average(diffs_data, window)
        diffs_data = running_average(diffs_data, window)

        # calculate the minimum rate of change from THIS smoothed data. append this range to the data. Highcharts
        # will display this as +/- ve bars on the chart
        diffs_data = calculate_minmax_values(diffs_data)

        # add the CSV file headers
        headerstring = "Date/time UTC, Min for hour, Max for hour, dH/dt"
        diffs_data.reverse()
        diffs_data.append(headerstring)
        diffs_data.reverse()

        # Save out the diffs array
        savevalues(k.FILE_4DIFFS, diffs_data)
