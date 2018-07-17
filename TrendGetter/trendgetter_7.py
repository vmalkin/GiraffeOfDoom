import os
import time
from datetime import datetime
from time import mktime
import re
import math

BIN_SIZE = 60 * 60 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total
STORM_THRESHOLD = 14
aurora_sightings_list = "sightings.csv"

class DP_Initial():
    def __init__(self, posixdate, data):
        self.posixdate = posixdate
        self.data = data

    def print_values(self):
        returnstring = str(self.posixdate) + "," + str(self.data)
        return returnstring

class DP_Publish():
    def __init__(self, posixdate, data):
        self.null = "#n/a"
        self.posixdate = posixdate
        self.data = data
        self.storm_threshold = self.null
        self.aurora_sighted = self.null
        self.carrington_point = self.null

    def posix2utc(self):
        utctime = time.gmtime(int(float(self.posixdate)))
        utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
        return utctime

    def print_values(self):
        returnstring = str(self.posix2utc()) + "," + str(self.data) + "," + str(self.storm_threshold) + "," + str(self.aurora_sighted) + "," + str(self.carrington_point)
        return returnstring
#
class DataBin():
    """DataBin - This objects allows us to crate a bin of values.
    Calculates the average value of the bin"""
    def __init__(self, posixdate):
        self.posixdate = posixdate
        self.datalist = []

    def dhdt_datalist(self):
        if len(self.datalist) >= 3:
            min = self.datalist[0]
            for i in range(0, len(self.datalist)):
                if float(self.datalist[i]) <= float(min):
                    min = float(self.datalist[i])

            max = self.datalist[0]
            for i in range(0, len(self.datalist)):
                if float(self.datalist[i]) >= float(max):
                    max = float(self.datalist[i])
            dhdt = round((max - min),4)
        else:
            dhdt = 0

        return dhdt

    def average_datalist(self):
        avgvalue = 0

        if len(self.datalist) > 0:
            for item in self.datalist:
                avgvalue = float(avgvalue) + float(item)

            avgvalue = avgvalue / float(len(self.datalist))
            avgvalue = round(avgvalue, 2)
        else:
            avgvalue = 0
        return avgvalue

    def print_values(self):
        returnstring = str(self.posixdate) + "," + str(self.dhdt_datalist())
        return returnstring


# ##################################################
# Binning - this is essentially a hash function based
# on the posix datetime
# ##################################################
def create_bins(objectlist):
    # we do NOT want decimal values for time, only ints
    date_now = int(time.time())

    # just while we work with the short dataset. Otherwise comment out
    # date_now = int(1528934391)

    date_start = date_now - 31536000

    binned_data = []
    for i in range(date_start, date_now, BIN_SIZE):
        dp = DataBin(i)
        binned_data.append(dp)

    # THis is the hashing function to drop data into the correct bins
    # according to the date.
    for i in range(0, len(objectlist)):
        bin_id = (float(objectlist[i].posixdate) - float(date_start)) / BIN_SIZE
        bin_id = int(round(bin_id,0))
        binned_data[bin_id].datalist.append(objectlist[i].data)
    return binned_data


# ##################################################
# median filter this works on a CSV list [datetime, data]
# ##################################################
def medianfilter(datalist):
    returnlist = []
    for i in range(1, len(datalist) - 1):
        templist = []
        datasplit_v1 = datalist[i - 1].split(",")
        datasplit_v2 = datalist[i].split(",")
        datasplit_v3 = datalist[i + 1].split(",")


        v1 = datasplit_v1[1]
        v2 = datasplit_v2[1]
        datetime = datasplit_v2[0]
        v3 = datasplit_v3[1]

        templist.append(v1)
        templist.append(v2)
        templist.append(v3)
        templist.sort()

        datavalue = templist[1]
        dp = datetime + "," + datavalue

        returnlist.append(dp)
    return returnlist

def utc_2_unix(utctime):
    print("Converting time to UNIX time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d"
    newdatetime = datetime.strptime(utctime,dateformat)
    # convert to Unix time (Seconds)
    newdatetime = mktime(newdatetime.timetuple())
    return newdatetime


# ##################################################
# add storm data to dH / dt
# ##################################################
def storm_threshold(dhdtlist):
    returnlist = dhdtlist
    for item in returnlist:
        if item.data >= STORM_THRESHOLD:
            item.storm_threshold = STORM_THRESHOLD
    return returnlist

# ##################################################
# add aurora sightings to dH / dt
# ##################################################
def aurora_sightings(dhdtlist):
    returnlist = dhdtlist
    posixdates = []

    with open(aurora_sightings_list) as e:
        for line in e:
            date = line.strip()  # remove any trailing whitespace chars like CR and NL
            dt = utc_2_unix(date)
            posixdates.append(dt)


    return returnlist

# ##################################################
# add carrington marker to dH / dt
# ##################################################
def carrington_marker(dhdtlist):
    returnlist = dhdtlist
    return returnlist


# ##################################################
# Write out values to file.
# ##################################################
def save_csv(arraydata, savefile):
    try:
        os.remove(savefile)
    except:
        print("Error deleting old file")

    for item in arraydata:
        try:
            with open(savefile, 'a') as f:
                f.write(item.print_values() + "\n")

        except IOError:
            print("WARNING: There was a problem accessing heatmap file")

# # #################################################################################
# # Create the smoothed data array and write out the files for plotting.
# # We will do a running average based on the running average time in minutes and the number
# # readings per minute
# # Data format is the DhdtData class in this file.
# # #################################################################################
# def running_average(input_array, averaging_interval):
#     displayarray = []
#
#     while len(input_array) > averaging_interval:
#         for i in range(averaging_interval + 1, len(input_array)):
#             datavalue = 0
#             datetime = input_array[i].posix_date
#
#             for j in range(0, averaging_interval):
#                 newdata = input_array[i-j].data_value
#                 datavalue = datavalue + newdata
#
#             datavalue = round((datavalue / averaging_interval), 3)
#             appendvalue = DhdtData(datetime, datavalue)
#             displayarray.append(appendvalue)
#
#     return displayarray
def create_dhdt(filtered_datalist):
    returnlist = []
    dhdt_threshold = 5
    for i in range(1,len(filtered_datalist)):
        prevsplit = filtered_datalist[i-1].split(",")
        nowsplit = filtered_datalist[i].split(",")

        prev_data = float(prevsplit[1])
        now_data = float(nowsplit[1])
        now_datetime = nowsplit[0]

        dhdt = now_data - prev_data
        if math.sqrt(math.pow(dhdt,2)) > dhdt_threshold:
            dhdt = 0

        dp = str(now_datetime) + "," + str(dhdt)
        returnlist.append(dp)

    return returnlist

# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
# Data format is the DhdtData class in this file.
# #################################################################################
def running_average(input_array, averaging_interval):
    displayarray = []

    while len(input_array) > averaging_interval:
        for i in range(averaging_interval + 1, len(input_array)):
            datavalue = 0
            datetime = input_array[i].posix_date

            for j in range(0, averaging_interval):
                newdata = input_array[i-j].data_value
                datavalue = datavalue + newdata

            datavalue = round((datavalue / averaging_interval), 3)
            appendvalue = DhdtData(datetime, datavalue)
            displayarray.append(appendvalue)

    return displayarray

# ##################################################
#
# S C R I P T   B E G I N S   H E R E
#
# ##################################################
# using the list of files, open each logfile into the main array

if __name__ == "__main__":
    # calculate the processing time
    starttime = datetime.now()
    starttime = mktime(starttime.timetuple())

    CSVlist = "files.txt"
    CSVFilenames = []
    rawdatalist = []
    print("Loading list of logfiles...")
    # load in the list of CSV files to process
    if os.path.isfile(CSVlist):
        try:
            with open(CSVlist) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    CSVFilenames.append(line)

        except IOError:
            print("List of logfiles appears to be present, but cannot be accessed at this time. ")

    print("Adding logfile data...")
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
            print("A logfile appears to be present, but cannot be accessed at this time. ")

    # Out data should be in the format of timestamp, data1, data2, etc We only need the timestamp and the
    # first data value
    # convert the list into an array of datapoint objects, with posix timestamps
    print("Begin converting logfile data to [posixdate, data] format")
    regex = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d)'
    dateformat = "%Y-%m-%d %H:%M:%S.%f"
    initial_datalist = []
    errorcount = 0

    for item in rawdatalist:
        itemsplit = item.split(",")
        utcdate = itemsplit[0]
        datavalue = itemsplit[1]

        # if the date matches trhe regex format, attempt to convert to posix timestamp
        if re.match(regex, utcdate):
            newdatetime = datetime.strptime(utcdate, dateformat)
            # convert to Unix time (Seconds)
            newdatetime = mktime(newdatetime.timetuple())
            newdatetime = int(newdatetime)
            dp = str(newdatetime) + "," + str(datavalue)
            # dp = DP_Initial(newdatetime, datavalue)
            initial_datalist.append(dp)
        else:
            errorcount = errorcount + 1
    print(str(errorcount) + " errors in datetime encountered")

    # apply a median filter to this list.  We are still working with a list of values, not a list of objects
    # at this point
    print("Apply median filter to initial data")
    filtered_datalist = medianfilter(initial_datalist)

    # create the list of DHDT values
    filtered_datalist = create_dhdt(filtered_datalist)

    # Create the list of OBJECTS
    templist2 = []
    for item in filtered_datalist:
        datasplit = item.split(",")
        date = datasplit[0]
        data = datasplit[1]
        dp = DP_Initial(date, data)
        templist2.append(dp)

    dhdt_list = create_bins(templist2)

    # ######################################################
    # SMooth the list before final plotting
    dhdt_list = running_average(dhdt_list, 6)

    # ######################################################
    # create the final set of datapoints for publishing
    finallist = []
    for item in dhdt_list:
        datetime = item.posixdate
        datavalue = item.dhdt_datalist()
        dp = DP_Publish(datetime, datavalue)
        finallist.append(dp)



    # Append the Aurora and Storm threshold info
    finallist = storm_threshold(finallist)
    # finallist = aurora_sightings(finallist)
    # finallist = carrington_marker(finallist)

    # Save out data
    save_csv(finallist, "tg_dhdt.csv")

    print("FINISHED")