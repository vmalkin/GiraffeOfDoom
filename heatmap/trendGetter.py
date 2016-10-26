import os
import re
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

# Raw Data Format:
# Date/Time (UTC), Raw X, Raw Y, Raw Z
# 2016-10-10 00:00:26.19,-391.23,3349.61,1354.43
#
# working data format:
# Date/Time (UTC), Value


# for each file in list
# We might need some method to parse a datafile to see that the data 
# is valid, not noisy, has no blips, etc.

magrate = 4  # How many readings per minute from the magnetometer
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
        print("Smoothing " + str(i) + " of " + str(len(arraydata)) + " records.")
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
        print("Differencing " + str(i) + " of " + str(len(arraydata)) + " records.")

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
        dataline = arraydata[i].split(",")
        # print(dataline)
        datetime = dataline[0]
        datavalue = dataline[1]
        newdata = datetime + "," + datavalue
        print("Pruning " + str(i) + " of " + str(len(arraydata)) + " records.")
        outputarray.append(newdata)

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

    datalist = re.split(r'[\s,:,]', arraydata[0])
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
    print("File Saved")

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



# Convert the absolute readings into differences
print("Converting to differences...\n")
rawdatalist = diffs_data(rawdatalist)

# Smooth the diffs twice.
print("Smoothing data...\n")
rawdatalist = running_avg(rawdatalist, 10*magrate)
rawdatalist = running_avg(rawdatalist, 10*magrate)

# Convert the diffs into hourly max/mins
print("Finding Daily max/mins...\n")
rawdatalist = maxmin_readings(rawdatalist)

# Save
print("Saving datafile...\n")
save_csv(rawdatalist, "trend.csv")


# #################
# Matplotlib graph
# #################
print("Creating graph...\n")
labelslist = []
datalist = []

# smoothedlist = running_avg(rawdatalist, 120)

for item in rawdatalist:
    data = item.split(",")
    labelslist.append(data[0])
    datavalue = Decimal(data[1])
    datalist.append(datavalue)

plt.plot(datalist, color='#00f000')

plt.ylabel("Relative Activity")
plt.xlabel("Date")
plt.legend(["Daily Activity"])
plt.title("Geomagnetic activity from " + labelslist[0] + " to " + labelslist[len(labelslist) - 1] + "\n")
plt.xticks(range(len(datalist)), labelslist, size='small', rotation='vertical')
plt.show()
