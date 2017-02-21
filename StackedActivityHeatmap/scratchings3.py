

import math
from decimal import Decimal, getcontext
from datetime import datetime
from time import mktime
import os



# #################################################################################
# Bindata takes in an array, each element of the form (UnixDatetime, datavalue)
# IT IS ASSUMED that:
# The array is a complete set of sequential data for the time period specified. (There may be gaps in data)
# The oldest element is at the top of the list, the youngest at the bottom.
# rawdata is (unixtime, data) and binsize is the size of the bin in minutes
def bindiffs(rawdata):
    # setup the bin array based on binsize. The bins will start from now and go back 24 hours
    # get current UTC
    currentdt = datetime.utcnow()

    # Convert to UNIX time
    currentdt = mktime(currentdt.timetuple())
    binsteps = 60 * 60 * 24

    # set up the timestamps for the bins
    # most recent time is first
    binneddata = []
    for i in range (0, 24):
        binneddata.append(currentdt)
        currentdt = currentdt - binsteps

    # check thru the rawdata. for each bin determin if there is enough data
    # and if so, calc df/dt for the bin

    return binneddata


    # Parse thru the current data by timestamp

# #################################################################################
# Rawdata is in the format (UnixDatetime, data)
# the function will return an array of (UnixDatetime, binned_value))
# #################################################################################
def binsimple(rawdata):
    # setup the bin array based on binsize. The bins will start from now and go back 24 hours
    # get current UTC
    currentdt = datetime.utcnow()

    # Convert to UNIX time
    currentdt = mktime(currentdt.timetuple())

    # width of bin in seconds.
    binwidth = 60
    # how many bins in a day?
    binnum = int(86400 / binwidth)
    print("Bin width is " + str(binwidth) + " seconds. There are " + str(binnum) + " bins in a day")

    # Threshold value for binning. We need more that this number of datapoints per bin, to have a reasonable amount
    # of data
    threshold = 1

    # setup the binneddata array timestamps
    # Most recent time is first
    timestamps = []
    for i in range(0, binnum):
        timestamps.append(currentdt)
        currentdt = currentdt - binwidth

    # array for final binned values
    binneddata = []
    # Now parse thru the rawdata array
    for i in range(0, len(timestamps) - 1):
        nowtime = timestamps[i]
        prevtime = timestamps[i + 1]
        counter = float(1)
        datavalue = float(0.0)

        for j in range(0, len(rawdata)):
            datasplit = rawdata[j].split(",")

            # time value to check
            split_time = float(datasplit[0])

            # only dealing with a single data value
            split_data = datasplit[1]

            # If the item from rawdata is inside the bin timestamps then...
            if split_time < nowtime and split_time > prevtime:
                datavalue = datavalue + float(split_data)
                counter = counter + 1

        # Calculate the average reading for the bin. If there is no data, we need to return an empty bin
        if counter > threshold:
            datavalue = datavalue / counter
        else:
            datavalue = ""

        # Create the datapoint
        dp = str(nowtime) + "," + str(datavalue)

        # append the datapoint to the binned data array
        binneddata.append(dp)

    # the returned array has the most recent readings at index[0] Invert the
    # array so it is like a conventional list
    binneddata.reverse()
    return binneddata





# #################################################################################
# Calculate the differences
# This function will create an array of differences. each element is (unixtime, datavalue)
# IT IS ASSUMED THAT:
# The data being fed in has been padded out to account for gaps in readings, by creating the
# timeslots with empty values for the data values, at the appropriate time intervals.
# #################################################################################
def create_diffs(readings):
    diffsarray = []
    # This is a value for spikes that are false, or artificially caused
    NOISE_SPIKE = 3

    # If the array is of sufficient size...
    if len(readings) > 2:
        for i in range(1, len(readings)):
            # get the 2 data readings we need to calculate the differences
            nowdata = readings[i]
            nowdata = nowdata.split(",")
            datetime = nowdata[0]
            data_now = nowdata[1]

            olddata = readings[i - 1]
            olddata = olddata.split(",")
            data_old = olddata[1]

            # Calculate the difference figure we need
            diffdata = float(data_now) - float(data_old)

            # if the difference is abnormally large, then make it a zero.
            if math.sqrt(math.pow(diffdata, 2)) > NOISE_SPIKE:
                diffdata = 0

            dp = str(datetime) + "," + str(diffdata)

            diffsarray.append(dp)

    else:
        dp = ("0000-00-00 00:00", 0)
        diffsarray.append(dp)

    return diffsarray

# #################################################################################
# Create the raw datapoint array from the save file
# #################################################################################
def CreateRawArray():
    readings = []
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile("ArraySave.csv"):
        with open("ArraySave.csv") as e:
            for line in e:
                line = line.strip() # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                # See the datapoint object/constructor for the current values it holds.
                dp = values[0] + "," + values[1]+ "," + values[2]+ "," + values[3]
                readings.append(dp)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded. Using new array.")

    return readings

# #################################################################################
# Save the raw datapoint array to the save file
# #################################################################################
def SaveRawArray(readings):
    # export array to array-save file
        try:
            with open ("bins.csv", 'w') as w:
                for dataObjects in readings:
                    w.write(dataObjects + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + "bins.csv")


# ##################################################
# Convert timestamps in array to Unix time
# ##################################################
def utc2unix(arraylist):
    print("Converting time to UNIX time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d %H:%M:%S.%f"
    # dateformat = "%Y-%m-%d %H:%M"
    workingarray = []

    # convert array data times to unix time
    workingarray = []
    for item in arraylist:
        try:
            itemsplit = item.split(",")
            newdatetime = datetime.strptime(itemsplit[0],dateformat)
            # convert to Unix time (Seconds)
            newdatetime = mktime(newdatetime.timetuple())

            datastring = str(newdatetime) + "," + str(itemsplit[1])
            workingarray.append(datastring)
        except:
            print("Problem with this entry: " + str(itemsplit))

    return workingarray

# ####################################################################################
# converts the UTC timestamp to unix time. returns converted array.
# ####################################################################################
def unix2utc(dataarray):
    temparray = []

    # For each item in the submitted array...
    for item in dataarray:
        # Split and get the unix date from the actual data
        item = item.split(",")
        unixdate = float(item[0])
        arraydata = item[1]

        # Convert the unix date to UTC time
        utctime = datetime.fromtimestamp(int(unixdate)).strftime("%Y-%m-%d %H:%M")

        # Recombine with the data and append to the array to be returned. Voila!
        appenddata = str(utctime) + "," + arraydata
        temparray.append(appenddata)

    return temparray

testdata = CreateRawArray()
testdata = utc2unix(testdata)
testdata = binsimple(testdata)
testdata = unix2utc(testdata)

SaveRawArray(testdata)
for item in testdata:
    print(item)
