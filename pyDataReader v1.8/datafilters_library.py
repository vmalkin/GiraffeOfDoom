from decimal import Decimal, getcontext
import constants as k
import DataPoint
import re
import logging

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
    timeinterval = 6 # minutes

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
    AVERAGING_TIME = int(k.MAG_RUNNINGAVG_COUNT * k.MAG_READ_FREQ)
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
# Create binned minutely averages
# to be used for experimental data/sensor merge project
# #################################################################################
def binnedaverages(readings):
    # Get each datapoint to print out it's values. Use re to split this on spaces, commas, and semi colons.
    # ['2016-05-08', '03', '34', '37.61', '6.12', '-8.24', '62.82', '0', '0', '0']
    xAvg = Decimal(0)
    yAvg = Decimal(0)
    zAvg = Decimal(0)
    counter = 0
    binnedvalues = []

    # Open the readings array
    for j in range(0, len(readings)-1):
        # Get the first datapoint from the array, so we get the current minute...
        dpvalues = re.split(r'[\s,:]', readings[j].print_values())
        nowminute = dpvalues[2]
        datetime = dpvalues[0] + " " + dpvalues[1] + ":" + nowminute

        # get the value for the next minute
        dpvalues1 = re.split(r'[\s,:]', readings[j + 1].print_values())
        nextminute = dpvalues1[2]

        # We are still summing values...
        if nowminute == nextminute and counter < k.MAG_READ_FREQ - 1:
            xAvg = xAvg + Decimal(dpvalues[4])
            yAvg = yAvg + Decimal(dpvalues[5])
            zAvg = zAvg + Decimal(dpvalues[6])
            counter = counter + 1

        # we have added up all the values for the minute and done the correct num of iterations
        # based on the frequency of the magnetometers output
        elif nowminute != nextminute and counter == k.MAG_READ_FREQ - 1:
            xAvg = xAvg + Decimal(dpvalues[4])
            yAvg = yAvg + Decimal(dpvalues[5])
            zAvg = zAvg + Decimal(dpvalues[6])

            # print(nowminute + " " + str(xAvg))

            xAvg = xAvg / Decimal(k.MAG_READ_FREQ)
            yAvg = yAvg / Decimal(k.MAG_READ_FREQ)
            zAvg = zAvg / Decimal(k.MAG_READ_FREQ)

            dp = DataPoint.DataPoint(datetime, xAvg, yAvg, zAvg)
            binnedvalues.append(dp)

            xAvg = 0
            yAvg = 0
            zAvg = 0
            counter = 0

        # Otherwise we do not have the correct number of iterations for the minute, ignore this.
        else:
            xAvg = 0
            yAvg = 0
            zAvg = 0
            counter = 0

    # WRITE OUT to binned file.
    try:
        # print("Write to file " + dp.print_values())
        with open (k.FILE_BINNED_MINS, 'w') as b:
            for dataObjects in binnedvalues:
                # dataObjects.print_values()
                b.write(dataObjects.print_values() + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_BINNED_MINS)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_BINNED_MINS)