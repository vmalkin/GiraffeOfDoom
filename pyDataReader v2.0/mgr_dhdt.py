"""
This file is for the purposes of creating a display file of magnetometer readings - dF/dt
The returned file should have the smoothed rate of change, and the average background levels
the returned file is CSV format
"""
import constants as k
import os.path
import logging
import math
from decimal import Decimal, getcontext
from datetime import datetime
import time


# #################################################################################
# Calculate the differences
# This function will create an array of differences
# #################################################################################
def create_diffs_array(readings_array):
    diffsarray = []

    if len(readings_array) > 2:
        for i in range(1, len(readings_array)):
            diff_x = (Decimal(readings_array[i].raw_x) - Decimal(readings_array[i-1].raw_x))
            # Each IF statement checks to see if reading exceeds the spike value. If it does
            # then we change the reading to zero.
            if math.sqrt(math.pow(diff_x, 2)) > k.NOISE_SPIKE:
                diff_x = 0
                print("spike in differences detected")

            diff_y = (Decimal(readings_array[i].raw_y) - Decimal(readings_array[i-1].raw_y))
            if math.sqrt(math.pow(diff_y, 2)) > k.NOISE_SPIKE:
                diff_y = 0
                print("spike in differences detected")

            diff_z = (Decimal(readings_array[i].raw_z) - Decimal(readings_array[i-1].raw_z))
            if math.sqrt(math.pow(diff_z, 2)) > k.NOISE_SPIKE:
                diff_z = 0
                print("spike in differences detected")

            datadate = readings_array[i].dateTime
            dx = diff_x
            # dy = diff_y
            # dz = diff_z
            # dp = str(datadate) + "," + str(dx) + "," + str(dy)+ "," + str(dz)
            dp = str(datadate) + "," + str(dx)

            # dp = DataPoint.DataPoint(readings_array[i].dateTime,diff_x, diff_y, diff_z)
            diffsarray.append(dp)
    else:
        dp = "0000-00-00 00:00:00,0"
        diffsarray.append(dp)

    return diffsarray


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
            jdatasplit = input_array[i].split(",")
            jdatadate = jdatasplit[0]

            # This is where we average for the time i before and after i.
            for j in range(0, AVERAGING_TIME):
                datasplit = input_array[(i - AVERAGING_TIME_HALF) + j]
                datasplit = datasplit.split(",")
                xdata = datasplit[1]

                xvalue = xvalue + Decimal(xdata)

            xvalue = Decimal(xvalue / AVERAGING_TIME)

            displaypoint = jdatadate + "," + str(xvalue)
            displayarray.append(displaypoint)

    else:
        displayarray = input_array

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
    # create the array of dF/dt
    diffs_data = create_diffs_array(data_array)

    # smooth the diffs to show the trend. Two passes at 5 minutes is usually ok.
    window = k.MAG_READ_FREQ * 5
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
