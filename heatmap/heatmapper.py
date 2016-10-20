import os
import re
from decimal import Decimal, getcontext

# Raw Data Format:
# Date/Time (UTC), Raw X, Raw Y, Raw Z
# 2016-10-10 00:00:26.19,-391.23,3349.61,1354.43

# for each file in list
# We might need some method to parse a datafile to see that the data 
# is valid, not noisy, has no blips, etc.

dataplaceindex = 2
magrate = 4   # How many readings per minute from the magnetometer
rawdatafile = "test.csv"
rawdataarray = []

# ##################################################
# Prune Data - we only need Date, time and Raw X value.
# ##################################################
def prune_data(arraydata):
    outputarray = []
    for item in arraydata:
        # dataline = item.split(",")
        dataline = re.split(r'[\s,,]', item)
        newdata = dataline[0] + "," + dataline[1] + "," + dataline[dataplaceindex]
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

        datetime = nowdata[0] + "," + nowdata[1]
        # calculate the differences
        diff = Decimal(nowdata[dataplaceindex]) - Decimal(olddata[dataplaceindex])

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
        datetime = datetime[0] + "," + datetime[1]

        # calculate the avg either side of this time interval
        for j in range(0, window):
            diff = arraydata[i - half_window + j].split(",")
            diff = diff[dataplaceindex]
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
    getcontext().prec = 5
    outputarray = []

    # reverse the data array so that we start from now, and going back, we get activity for the last 60 mins
    arraydata.reverse()

    # this is an hour's worth of readings in our array
    interval = 60 * magrate
    for i in range(0, len(arraydata), interval):
        maxvalue = 0
        minvalue = 0
        # get the datetime for the hour
        datetime = arraydata[i].split(",")
        datetime = datetime[0] + "," + datetime[1]

        if i + interval < len(arraydata):
            for j in range(0, interval):
                k = i + j
                hvalue = arraydata[k].split(",")
                # print(str(k))
                hvalue = Decimal(hvalue[dataplaceindex])
                if hvalue >= minvalue and hvalue <= maxvalue:
                    pass # everything is ok

                if hvalue >= maxvalue and hvalue >= minvalue:
                    maxvalue = hvalue # this reading is largest

                if hvalue <= maxvalue and hvalue <=  minvalue:
                    minvalue = hvalue # this reading is smallest

        diff = maxvalue - minvalue

        differencevalues = datetime + "," + str(diff)
        outputarray.append(differencevalues)

    # Revert the output array so it plots conventionally, oldest to most recent
    outputarray.reverse()
    return outputarray

# ##################################################
# Write out values to file.
# ##################################################
def save_csv(arraydata, savefile):
    try:
        os.remove(savefile)
    except:
        print("Error deleting old file")
    for line in arraydata:
        try:
            with open(savefile, 'a') as f:
                f.write(line + "\n")
        except IOError:
            print("WARNING: There was a problem accessing heatmap file")

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
# Normalise data
# ##################################################
def normalise(arraydata):
    # Normalise single value data
    temp_array = []

    datamin = Decimal(1000)
    # first find the smallest value...
    for item in arraydata:
        item = item.split(",")
        # this is now the actual value figure...
        item = Decimal(item[dataplaceindex])
        if item <= datamin:
            datamin = item

    datamax = Decimal(datamin)
    # now find the largets value...
    for item in arraydata:
        item = item.split(",")
        # this is now the actual value figure...
        item = Decimal(item[dataplaceindex])
        if item > datamax:
            datamax = item

    temp_array = []

    print("max/min values: " + str(datamax) + "/" + str(datamin))

    diffvalue = datamax - datamin
    for i in range(0, len(arraydata)):
        datastring = arraydata[i].split(",")
        datavalue = (Decimal(datastring[dataplaceindex]) - datamin) / diffvalue
        newdatastring = datastring[0] + "," + datastring[1] + "," + str(datavalue)
        temp_array.append(newdatastring)

    return temp_array

# ##################################################
# M A I N   C O D E   S T A R T S  H E R E
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

# normalise the data for consistent display
rawdataarray = normalise(rawdataarray)

# save the file
save_csv(rawdataarray, "heatmap.csv")

