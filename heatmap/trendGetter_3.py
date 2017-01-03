import os
import re
# import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
from datetime import datetime
from time import mktime

# Raw Data Format:
# Date/Time (UTC), Raw X, Raw Y, Raw Z
# 2016-10-10 00:00:26.19,-391.23,3349.61,1354.43
#
# working data format:
# Date/Time (UTC), Value


# for each file in list
# We might need some method to parse a datafile to see that the data 
# is valid, not noisy, has no blips, etc.

maginterval = 15 # how many seconds between each reading
magrate = int(60 / maginterval)
eventthreshold = 1.6


# ##################################################
# Running Average - smooth diffs
# ##################################################
def running_avg(arraydata, interval):
    getcontext().prec = 5
    outputarray = []

    #calculate thje running avg window size
    window = interval
    half_window = int(window / 2)

    for i in range(half_window, (len(arraydata) - half_window)):
        avgdiff = 0

        # get the datetime
        datetime = arraydata[i].split(",")
        datetime = datetime[0]

        # calculate the avg either side of this time interval
        for j in range(0, window):
            value = arraydata[i - half_window + j].split(",")
            value = value[1]
            avgdiff = avgdiff + Decimal(value)

        avgdiff = Decimal(avgdiff / window)

        # create the data string to be written to list
        datastring = datetime + "," + str(avgdiff)
        # print("Smoothing " + str(i) + " of " + str(len(arraydata)) + " records.")
        outputarray.append(datastring)

    # print("Array is " + str(len(arraydata)) + " records long")
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
        datetime = nowdata[0]
        nowdata = Decimal(nowdata[1])

        olddata = arraydata[i - 1].split(",")
        olddata = Decimal(olddata[1])

        # calculate the differences
        diff = nowdata - olddata

        # create the string to be appended
        outputline = datetime + "," + str(diff)

        outputarray.append(outputline)
        # print("Differencing " + str(i) + " of " + str(len(arraydata)) + " records.")

    # return array of differences
    # print("Array is " + str(len(arraydata)) + " records long")
    return outputarray

# ##################################################
# Prune Data - we only need Raw X value.
# ##################################################
def prune_data(arraydata):
    outputarray = []
    # we want to avoid the first line that contains a header text
    for i in range(0,len(arraydata)):
        try:
            dataline = arraydata[i].split(",")
            # print(dataline)
            datetime = dataline[0]
            datavalue = dataline[1]
            newdata = datetime + "," + datavalue
            # print("Pruning " + str(i) + " of " + str(len(arraydata)) + " records.")
            outputarray.append(newdata)
        except:
            print("There is a problem with this data value - isolate the log file it belongs to and check: ")
            print("--> " + str(arraydata[i-1]))
            print("--> " + str(arraydata[i]))
            print("--> " + str(arraydata[i + 1]))

    return outputarray

# ##################################################
# Daily Activity - create max/min values for an array
# and return the difference
# Date/Time (UTC), Raw X
# 2016-10-10 00:00:26.19,-391.23
# ###################################################
def maxmin_readings(arraydata):
    getcontext().prec = 5
    maxvalue = 0
    minvalue = 0

    datalist = re.split(r'[\s,:]', arraydata[0])
    olddate = datalist[0]
    oldhour = datalist[1]

    returndata = []

    # We want to grab an hours worth of data from the arraydata based on the timestamps
    for i in range(1,len(arraydata)):
        # get the current values from the present item
        datalist = re.split(r'[\s,:,]', arraydata[i])
        currentdate = datalist[0]
        currenthour = datalist[1]
        datavalue = datalist[4]

        # print(currentdate + " / " + olddate + " " + currenthour + " / " + oldhour)

        # if the current date is the same as the old date, and the current hour is the same as the old hour
        # then do the comparison
        # if olddate == currentdate and oldhour == currenthour:
        if olddate == currentdate:
            datavalue = Decimal(datavalue)
            if datavalue >= minvalue and datavalue <= maxvalue:
                pass  # everything is ok

            if datavalue >= maxvalue and datavalue >= minvalue:
                maxvalue = datavalue  # this reading is largest

            if datavalue <= maxvalue and datavalue <= minvalue:
                minvalue = datavalue  # this reading is smallest

            # else we have moved into the next hour/date. Append the current values to the ouput array if we have the
            # minimum amount of data. Reset the old hour/date
        else:
            diff = maxvalue - minvalue
            outputdate = arraydata[i].split(",")
            outputdate = outputdate[0]

            outputstring = outputdate + "," + str(diff)
            returndata.append(outputstring)

            olddate = currentdate
            # oldhour = currenthour
            maxvalue = 0
            minvalue = 0

    # return the new hourly array
    return returndata


# ##################################################
# This function is designed to pad out the data array
# to the correct length in case we're missing data
# from any of the log files, or missing comlete logfiles.
# missing data will be zeros.
#
# The array timestamps will be in UNIX time.
# ##################################################
def correct_days(arraydata):
    # set date time format for strptime()
    # dateformat = "%Y-%m-%d %H:%M:%S.%f"

    # Get the start and finish datetimes
    startdate = arraydata[0].split(",")
    enddate = arraydata[len(arraydata) - 1].split(",")

    startdate = int(float(startdate[0]))
    enddate = int(float(enddate[0]))

    # the start dates and end dates are now UNIX style datestamps (Seconds)
    # there are 3600 seconds in an hour and 86400 sec in a day

    workingarray = []

    # Determine the real length of time between the start date and end date. Divide this into magnetometer read intervals
    # this will become the new array with gaps where there is zero data.
    duration = enddate - startdate
    magreadingscount = int(duration / maginterval)

    correctedarray = []

    for i in range(startdate, enddate, magreadingscount):
        appendflag = 0
        for j in range(0, len(workingarray)):
            datasplit = workingarray[j].split(",")

            # if there is an entry in the raw data that matches a slot in the corrected array...
            if float(datasplit[0]) >= i and float(datasplit[0]) < i + magreadingscount:
                correctedarray.append(workingarray[j])
                appendflag = 1

        # Otherwise there is no entry that maps to ne timeslot. So this will be a zero entry for this timeslot
        if appendflag == 0:
            appendstring = str(i) + ",0"
            correctedarray.append(appendstring)

    return arraydata


# ##################################################
# Convert timestamps in array to Unix time
# ##################################################
def array_days_to_unix(arraylist):
    print("Converting time to UNIX time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d %H:%M:%S.%f"
    workingarray = []

    # convert array data times to unix time
    workingarray = []
    for item in arraylist:
        try:
            datasplit = item.split(",")

            newdatetime = datetime.strptime(datasplit[0],dateformat)
            # convert to Unix time (Seconds)
            newdatetime = mktime(newdatetime.timetuple())

            datastring = str(newdatetime) + "," + datasplit[1]
            workingarray.append(datastring)
        except:
            print("Problem with this entry: " + item)

    return workingarray

# ##################################################
# Convert timestamps in array to UTC time
# ##################################################
def array_days_to_utc(arraylist):
    print("Converting time to UTC time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d %H:%M:%S.%f"

    # Convert the date string to the format of: 2016-10-10 00:00:26.19
    returnarray = []

    for item in arraylist:
        datasplit = item.split(",")
        unixdate = int(float(datasplit[0]))

        # Convert the UNix timestamp, inot a UTC string
        utcdate = datetime.fromtimestamp(unixdate)

        # Create the dataline to be appended
        dataline = str(utcdate) + "," + datasplit[1]
        returnarray.append(dataline)

    return returnarray


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
# Normalise the data
# ##################################################
def normalise(arraydata):
    minvalue = Decimal(10000)

    # find the max and min values
    for item in arraydata:
        datasplit = item.split(",")
        # If the current item value is less than the current minimum value, make the appropriate change
        if Decimal(datasplit[1]) < Decimal(minvalue):
            minvalue = Decimal(datasplit[1])

    # now find the max value
    maxvalue = minvalue
    for item in arraydata:
        datasplit = item.split(",")
        if Decimal(datasplit[1]) > Decimal(maxvalue):
            maxvalue = datasplit[1]

    # formula for normalising data is (x - min) / (max - min)
    temparray =[]
    for item in arraydata:
        datasplit = item.split(",")
        timestamp = datasplit[0]
        reading = Decimal(datasplit[1])

        nrmlview = (reading - minvalue) / (Decimal(maxvalue) - Decimal(minvalue))

        datastring = timestamp + "," + str(nrmlview)
        temparray.append(datastring)

    return temparray

# ##################################################
# Display Carrington Cycle
# the data should have the format of datetime, normalised_data
# ##################################################
def carrington_cycle(arraydata):
    temparray = []
    # we are using an average figure of 2 days either side, so 5 days inclusive
    window = 5
    interval = int((window - 1) / 2)

    if len(arraydata) > window:
        for i in range(interval, len(arraydata) - interval):
            avgdata = 0

            for j in range(i - interval, i + interval):
                datasplit = arraydata[j].split(",")
                avgdata = avgdata + Decimal(datasplit[1])

            avgdata = Decimal(avgdata/window)
            tempdatastring = arraydata[i] + "," + str(avgdata)
            temparray.append(tempdatastring)

        return temparray
    else:
        return arraydata


# ##################################################
# Peak detecting function. This function will
# identify peaks in data and append a new column.
# Peaks will have a value of 1, otherwise 0.
# ##################################################
def peek_a_chu(arraydata):
    peakdates = []
    halfwindow = 1   # our window is +/- days either side of the date we are checking

    if len(arraydata) <= (halfwindow * 2):
        print("Array too small to compute peak dates")
    else:
        for i in range(halfwindow, len(arraydata) - halfwindow):
            preindex = arraydata[i - halfwindow].split(",")
            nowindex = arraydata[i].split(",")
            postindex = arraydata[i + halfwindow].split(",")

            nowdate = nowindex[0]
            # The smoothed curve is the second index in the split
            preindex = preindex[2]
            nowindex = nowindex[2]
            postindex = postindex[2]

            # If we are at the "top of the hill"
            if preindex <= nowindex and postindex <= nowindex:
                print(nowdate)
                peakdates.append((nowdate))

    if len(peakdates) > 0:
        return peakdates
    else:
        return "No peak dates found"

# ##################################################
# this function will forcast future dates for max
# carrington cycle. We should show
# ##################################################
def predict_cycle(arraydata):
    pass

# ##################################################
# M A I N   C O D E   S T A R T S  H E R E
# ##################################################
CSVlist = "files.txt"
CSVFilenames = []
rawdatalist = []

# load in the list of CSV files to process
if os.path.isfile(CSVlist):
    try:
        with open(CSVlist) as e:
            for line in e:
                line = line.strip()  # remove any trailing whitespace chars like CR and NL
                CSVFilenames.append(line)

    except IOError:
        print("File appears to be present, but cannot be accessed at this time. ")

# Parse thru the CSVfilelist, Append values to our raw data list
for item in CSVFilenames:
    firstline = True
    try:
        with open(item) as e:
            print("Processing " + item)
            # Skip the first line in each file as it's a header
            for line in e:
                if firstline == True:
                    # print("Header identified, skipping...")
                    firstline = False
                else:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    rawdatalist.append(line)

    except IOError:
        print("File appears to be present, but cannot be accessed at this time. ")

# Prune the raw data list down to a date and value only
# for item in rawdatalist:
#     print(item)
print("Reducing data...\n")
rawdatalist = prune_data(rawdatalist)

# At this point - verify that we have the full number of consecutive days between starts and end dates in the list
# Parse thru and create corrected list as necessary
# The best way to do this is to reduce the magnetomter data down to whole minutes, pad out empty mins with zeros
# then procede to calculate the differences as usual

# COnvert the timestamps to UNIX time
rawdatalist = array_days_to_unix(rawdatalist)

# Correct for missing days
rawdatalist = correct_days(rawdatalist)

# Convert the absolute readings into differences
print("Converting to differences...\n")
rawdatalist = diffs_data(rawdatalist)

# Smooth the diffs twice.
print("Smoothing, pass 1...")
rawdatalist = running_avg(rawdatalist, 10 * magrate)
print("Smoothing, pass 2...")
rawdatalist = running_avg(rawdatalist, 10 * magrate)

# COnvert the array back to UTC time
rawdatalist = array_days_to_utc(rawdatalist)

# Convert the diffs into Daily max/mins
# this will work on the timestamps in the array
print("Finding Daily max/mins...\n")
rawdatalist = maxmin_readings(rawdatalist)

# Normalise the readings
print("Normalising data...")
rawdatalist = normalise(rawdatalist)

# Create the 5 day average of readings, and append this to the correct date
# this displays the carrington cycle
print("Creating Carrington Cycle data...")
rawdatalist = carrington_cycle(rawdatalist)


# Use a peak finding algorythm. Write peak dates out to somewhere else and predict new dates
peakdata = peek_a_chu(rawdatalist)

# Save
print("Saving datafile...\n")
save_csv(rawdatalist, "trenddata.csv")
save_csv(peakdata, "peakdata.csv")


#################
# Matplotlib graph
#################
# print("Creating graph...\n")
# labelslist = []
# datalist = []
#
# for item in rawdatalist:
#     data = item.split(",")
#     # we need to truncate the label on the space in the datetime string
#     label = str(data[0]).split(" ")
#     label = label[0]
#     labelslist.append(str(label))
#
#     # append data to the data array
#     datavalue = Decimal(data[1]) + Decimal(data[2])
#     datalist.append(datavalue)
#
# plt.plot(datalist, color='#00f000')
#
# plt.ylabel("Relative Activity")
# plt.xlabel("Date")
# plt.legend(["Daily Activity"])
# plt.title("Geomagnetic activity from " + labelslist[0] + " to " + labelslist[len(labelslist) - 1] + "\n")
# plt.xticks(range(len(datalist)), labelslist, size='small', rotation='vertical')
# plt.show()
