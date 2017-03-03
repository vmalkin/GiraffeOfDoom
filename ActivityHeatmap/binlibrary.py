import constants as k
from datetime import datetime
from time import mktime



# #################################################################################
# Rawdata is in the format (UnixDatetime, data)
# the function will return an array of (UnixDatetime, binned_value))
# #################################################################################
def bin_dh_dt(rawdata):
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
    # Most recent time is first. Count back from current time in binwidths and append the time to the list
    timestamps = []
    for i in range(0, binnum):
        timestamps.append(currentdt)
        currentdt = currentdt - binwidth

    # array for final binned values
    binneddata = []

    # convert the raw data into dh/dt




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
    # Most recent time is first. Count back from current time in binwidths and append the time to the list
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
        counter = float(0)
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
            print(counter)
            datavalue = datavalue / counter

            # Create the datapoint
            dp = str(nowtime) + "," + str(datavalue)

            # append the datapoint to the binned data array
            binneddata.append(dp)

        # If there is no data, then no datapoint will be created.

        # the returned array has the most recent readings at index[0] Invert the
        # array so it is like a conventional list
    binneddata.reverse()

    return binneddata


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
    count = 0
    for i in range(0, len(arraylist)):
        try:
            itemsplit = arraylist[i].print_values().split(",")
            newdatetime = datetime.strptime(itemsplit[0],dateformat)
            # convert to Unix time (Seconds)
            newdatetime = mktime(newdatetime.timetuple())

            datastring = str(newdatetime) + "," + str(itemsplit[1])
            workingarray.append(datastring)
        except:
            count = count + 1
            print("Problem with entry " + count)

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
def SaveRawArray(readings):
    # export array to array-save file
    try:
        with open(k.FILE_BINNED_MINS, 'w') as w:
            for dataObjects in readings:
                w.write(dataObjects + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + k.FILE_BINNED_MINS)

# typically we would have
# array = utc2unix(array)
# array = binsimple(array)
# array = unix2utc(array)