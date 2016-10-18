import os
from decimal import Decimal, getcontext

# Raw Data Format:
# Date/Time (UTC), Raw X, Raw Y, Raw Z
# 2016-10-10 00:00:26.19,-391.23,3349.61,1354.43

# for each file in list
# We might need some method to parse a datafile to see that the data 
# is valid, not noisy, has no blips, etc.


magrate = 4   # How many readings per minute from the magnetometer
rawdatafile = "C:/Users/vaughnm.OPNET/Desktop/GitHub/GiraffeOfDoom/heatmap/test.csv"
rawdataarray = []

# ##################################################
# Prune Data - we only need Datetime and Raw X value.
# ##################################################
def prune_data(arraydata):
    outputarray = []
    for item in arraydata:
        dataline = item.split(",")
        newdata = dataline[0] + "," + dataline[1]
        outputarray.append(newdata)

    return outputarray

# ##################################################
# Diffs Data - convert X values to differences.
# ##################################################
def diffs_data(arraydata):
    getcontext().prec = 5
    outputarray = []

    # Parse thru the input array
    for i in range(1, len(arraydata)):
        # grab the reading for now and the last reading
        nowdata = arraydata[i].split(",")
        olddata = arraydata[i - 1].split(",")

        datetime = nowdata[0]
        # calculate the differences
        diff = Decimal(nowdata[1]) - Decimal(olddata[1])

        # create the string to be appended
        outputline = datetime + "," + str(diff)

        outputarray.append(outputline)

    # return array of differences
    return outputarray


# ##################################################
# Running Average - smooth diffs
# ##################################################
def running_avg(arraydata):
    getcontext().prec = 5
    outputarray = []

    # for 10 min interval
    interval = 10

    #calculate thje running avg window size
    window = interval * magrate
    half_window = int(window / 2)

    for i in range(half_window, (len(arraydata) - half_window)):
        avgdiff = 0

        # get the datetime
        datetime = arraydata[i].split(",")
        datetime = datetime[0]

        # calculate the avg either side of this time interval
        for j in range(0, window):
            diff = arraydata[i - half_window + j].split(",")
            diff = diff[1]
            avgdiff = avgdiff + Decimal(diff)

        avgdiff = Decimal(avgdiff / window)

        # create the data string to be written to list
        datastring = datetime + "," + str(avgdiff)

        outputarray.append(datastring)

    return outputarray


# ##################################################
# Hourly Activity - create activity readings for the hour
# ###################################################
def hourly_readings(arraydata):
    outputarray = []

    # reverse the data array so that we start from now, and going back, we get activity for the last 60 mins
    arraydata.reverse()

    # this is an hour's worth of readings in our array
    interval = 60 * magrate
    for i in range(0, len(arraydata), interval):
        maxvalue = 100
        minvalue = -100

        # get the datetime for the hour
        datetime = arraydata[i].split(",")
        datetime = datetime[0]

        for j in range (0, interval):
            # determin the max and min values



    # Revert the output array so it plots conventionally, oldest to most recent
    outputarray.reverse()

# ##################################################
# Write out values to file.
# ##################################################
def save_csv(arraydata):
    pass

# ##################################################
# Median Filter
# ##################################################
def median_filter_3values(arraydata):
    outputarray = []

    for i in range(1, len(arraydata)-1):
        xlist = []

        for j in range(-1, 2):    # -1, 0, 1
            k = i + j
            xlist.append(arraydata[k].raw_x)

        xlist.sort()

        outputarray.append(dp)

    return outputarray

# ##################################################
# MAIN CODE STARTS HERE
# ##################################################

# Load in CSV data
if os.path.isfile(rawdatafile):
    try:
        with open(rawdatafile) as e:
            for line in e:
                line = line.strip()  # remove any trailing whitespace chars like CR and NL
                rawdataarray.append(line)

    except IOError:
        print("File appears to be present, but cannot be accessed at this time. ")

# Prune down rawdataarray to datetime and X values
rawdataarray = prune_data(rawdataarray)

# Convert list of absolute values into dH/dt
rawdataarray = diffs_data(rawdataarray)

# Smooth the array down
rawdataarray = running_avg(rawdataarray)
rawdataarray = running_avg(rawdataarray)

# create the hourly readings
rawdataarray = hourly_readings(rawdataarray)

# save the file
save_csv(rawdataarray)

