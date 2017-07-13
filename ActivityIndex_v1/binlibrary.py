import constants as k
from datetime import datetime
from time import mktime
import math

# #################################################################################
# Rawdata is in the format (UnixDatetime, data)
# the function will return an array of (UnixDatetime, dH/dt)
# #################################################################################
def make_dhdt(rawdata):
    returnarray = []

    for i in range(1, len(rawdata)):
        olddata = rawdata[i - 1].split(",")
        nowdata = rawdata[i].split(",")

        nowtime = nowdata[0]
        dhdt = float(nowdata[1]) - float(olddata[1])
        dp = nowtime + "," + str(dhdt)

        returnarray.append(dp)

    return returnarray


# #################################################################################
# Rawdata is in the format (UnixDatetime, data)
# the function will return an array of (binned_value))
# #################################################################################
def bin_dh_dt(rawdata):
    # setup the bin array based on binsize. The bins will start from now and go back 24 hours
    # get current UTC
    currentdt = datetime.utcnow()

    # Convert to UNIX time
    currentdt = mktime(currentdt.timetuple())

    # width of bin in seconds.
    binwidth = 60 * 60

    # how many bins in a day?
    binnum = int(86400 / binwidth)
    print("Bin width is " + str(binwidth) + " seconds. There are " + str(binnum) + " bins in a day")

    # Threshold value for binning. We need more that this number of datapoints per bin, to have a reasonable amount
    # of data
    threshold = 1

    # setup the binneddata array timestamps
    # the array goes from index[now] -> index[time is oldest]
    timestamps = []
    for i in range(0, binnum):
        timestamps.append(currentdt)
        currentdt = currentdt - binwidth

    # array for final binned values
    binneddata = []

    # parse thru the data array, assigning the correct values to the bins
    for i in range (0, len(timestamps) - 1):
        nowtime = timestamps[i]
        prevtime = timestamps[i + 1]
        maxv = float(-1000)
        minv = float(1000)

        # GO thru the raw data and check for max-min H readings and calculate the rate of change for the bin
        for j in range(0, len(rawdata)):
            datasplit = rawdata[j].split(",")
            datadate = float(datasplit[0])
            datavalue = float(datasplit[1])

            # if the data falls into the range of the bin, determine if its a max or min value
            if datadate < nowtime and datadate > prevtime:
                # determin max and min values for this window interval
                if datavalue >= maxv:
                    maxv = datavalue
                elif datavalue <= minv:
                    minv = datavalue

        # determin dH/dt for the bin period append to the bin array
        # null data will manifest as a large minus value, so we discount it
        hvalue = maxv - minv
        if hvalue < -500:
            binneddata.append(k.NULLBIN)
        else:
            binneddata.append(hvalue)

    # the returned data goes from index[now] -> index[time is oldest]
    return binneddata


# ##################################################
# Convert timestamps in array to Unix time
# ##################################################
def utc2unix(arraylist):
    print("Converting time to UNIX time...")
    # set date time format for strptime()
    # dateformat = "%Y-%m-%d %H:%M:%S.%f"
    # dateformat = '"%Y-%m-%d %H:%M:%S"'
    dateformat = '%Y-%m-%d %H:%M'
    workingarray = []

    # convert array data times to unix time
    workingarray = []
    count = 0
    for i in range(0, len(arraylist)):
        try:
            itemsplit = arraylist[i].split(",")
            newdatetime = datetime.strptime(itemsplit[0],dateformat)
            # convert to Unix time (Seconds)
            newdatetime = mktime(newdatetime.timetuple())

            datastring = str(newdatetime) + "," + str(itemsplit[1])
            workingarray.append(datastring)
        except:
            count = count + 1
            print("UTC 2 Unix conversion - problem with entry " + str(count))

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

# #################################################################################
# Save the raw datapoint array to the save file
# #################################################################################
def SaveRawArray(readings, filename):
    # export array to array-save file
    try:
        with open(filename, 'w') as w:
            for dataObjects in readings:
                w.write(str(dataObjects) + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + filename)

# typically we would have
# array = utc2unix(array)
# array = binsimple(array)
# array = unix2utc(array)