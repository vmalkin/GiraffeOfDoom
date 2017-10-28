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
# The data is saved out to a CSV with the format [UNIX_time, accrued_min_values, count_of_averages]
# #################################################################################
def create_background_bars(diffs):
    gain = 1.3
    newdiffs = []

    # load up mins value from file from calculate_min_values()
    minbg = calculate_min_values(diffs)
<<<<<<< HEAD:pyDataReader v2.0/mgr_dhdt.py
    minbg = (minbg * gain) / 2
=======

    # create string of min data to be appended to diffs file. The value in the array is a range from low to high
    # so we will halve it and create two series of +ve and -ve values to create the max-min band in the graph.
    print(minbg)
    minbg = minbg[1] / 2

>>>>>>> origin/DnA-Service:pyDataReader v2.0/difference_creator.py

    for item in diffs:
        itemsplit = item.split(",")
        itemdate = itemsplit[0]
        itemdata = itemsplit[1]
        appendvalue = itemdate + "," + str(minbg) + "," + str(-1 * minbg) + "," + itemdata
        newdiffs.append(appendvalue)

    return newdiffs


# #################################################################################
# min values for an array of data will be the minimum dF/dt in any 60min interval
# within the data
# the format for the min value data is a list of one entry: [unix_date,min_value]
# #################################################################################
def calculate_min_values(diffs_data):
<<<<<<< HEAD:pyDataReader v2.0/mgr_dhdt.py
    # file has the format of one line [UTC_of_last_update, min_value]
    # saved_min_file = k.STATION_ID + "mins.csv"
    # stationmin = []
    # unix_timenow = time.time()
    #
    # # IF the min value file does not exist then...
    # if os.path.isfile(saved_min_file):
    #     with open(saved_min_file) as e:
    #         for line in e:
    #             line = line.strip()  # remove any trailing whitespace chars like CR and NL
    #             stationmin.append(line)
    #
    #     datasplit = stationmin.split(",")
    #     datadate = datasplit[0]
    #
    #     if (datadate + 86400) < unix_timenow:
    #         # recalc values[]
    #         pass
    # else:
    #     # recalc values[]
    #     pass
=======
    min_value_data = []
    hourrange = k.MAG_READ_FREQ * 60
    min_value = 1000000
    nowtime = datetime.utcnow()
    nowtime = time.mktime(nowtime.timetuple())
    calc_flag = False
    savefilename = k.STATION_ID + "mindata.csv"

    # IF the min value file does not exist then...
    # calculate min value of the current array
    # Create the min value array
    if os.path.isfile(savefilename):
       loadvalues(savefilename, min_value_data)
    else:
        print("No saved values. Calculating new min values")
        for i in range (0, len(diffs_data) - hourrange):
            minholder = float(1000000)
            maxholder = float(-1000000)
            for j in range(0, hourrange):
                checkdata = diffs_data[j + i].split(",")
                checkdata = checkdata[1]
                if float(checkdata) > float(maxholder):
                    maxholder = checkdata
                if float(checkdata) < float(minholder):
                    minholder = checkdata

            checkdata = float(maxholder) - float(minholder)

            if checkdata < min_value:
                min_value = checkdata

        appenddata = str(nowtime) + "," + str(min_value)
        min_value_data.append(appenddata)
        print("Min values done.")
>>>>>>> origin/DnA-Service:pyDataReader v2.0/difference_creator.py

    # IF more than 24 hours passed since the last calculation? Then
    # calculate min value of the current array
    # Create the min value array
<<<<<<< HEAD:pyDataReader v2.0/mgr_dhdt.py
=======
    storedsplit = min_value_data[0].split(",")
    storedtime = storedsplit[0]
    if (float(nowtime) - float(storedtime)) > (hourrange * 24):
        print("Over 24 hours. Re-calculating new min values")
        for i in range (0, len(diffs_data) - hourrange):
            minholder = 1000000
            maxholder = -1000000
            for j in range(0, hourrange):
                checkdata = diffs_data[j + i].split(",")
                checkdata = checkdata[1]
                if checkdata > maxholder:
                    maxholder = checkdata
                if checkdata < minholder:
                    minholder = checkdata

            checkdata = maxholder - minholder

            if checkdata < min_value:
                min_value = checkdata

        appenddata = str(nowtime) + "," + str(min_value)
        min_value_data.append(appenddata)
        print("Min values done.")
>>>>>>> origin/DnA-Service:pyDataReader v2.0/difference_creator.py

    # ELSE load the min values and create the min value array

    # save the min values to file
    # savevalues(saved_min_file, stationmin)

    min_data = 0.02
    return min_data


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
    diffs_data = create_background_bars(diffs_data)

    # add the CSV file headers
    headerstring = "Date/time UTC, Background, Background, dH/dt"
    diffs_data.reverse()
    diffs_data.append(headerstring)
    diffs_data.reverse()

    # Save out the diffs array
    savevalues(k.FILE_4DIFFS, diffs_data)
