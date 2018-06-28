import os
import time
from datetime import datetime
from time import mktime
import re
import math

BIN_SIZE = 60 * 60 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total
DHDT_THRESHOLD = 20

class DP_Initial():
    def __init__(self, posixdate, data):
        self.posixdate = posixdate
        self.data = data

class DP_Publish():
    def __init__(self, posixdate, data):
        self.null = "#n/a"
        self.posixdate = posixdate
        self.data = data
        self.storm_threshold = self.null
        self.aurora_sighted = self.null

    def posix2utc(self):
        utctime = time.gmtime(int(float(self.posixdate)))
        utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
        return utctime

    def print_values(self):
        returnstring = str(self.posix2utc()) + "," + str(self.data) + "," + str(self.storm_threshold) + "," + str(self.aurora_sighted)
        return returnstring

class DataBin():
    def __init__(self, posixdate):
        self.posixdate = posixdate
        self.datalist = []

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
        returnstring = str(self.posixdate) + "," + str(self.average_datalist())
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
# median filter this works on a CSV list
# ##################################################
def medianfilter(datalist):
    # objects in the array list have the format [posix_time, data]
    filteredlist = []
    window = 3
    arrayindex_date = int((window - 1) / 2)
    boundary = arrayindex_date

    for i in range(arrayindex_date, len(datalist) - boundary):
        datasplit = datalist[i].split(",")
        datetime = datasplit[0]
        temp_data = []

        for j in range((-1 * boundary), boundary + 1):
            datasplit = datalist[i + j].split(",")
            value = datasplit[1]
            temp_data.append(value)
        temp_data.sort()
        value = temp_data[arrayindex_date]
        dp = datetime + "," + value
        filteredlist.append(dp)
    return filteredlist


# ##################################################
# Convert straight magnetogram to dH / dt
# ##################################################
def create_dhdt(objectlist):
    returnlist = []

    for i in range(1, len(objectlist)):
        prev = float(objectlist[i-1].data)
        now = float(objectlist[i].data)
        dhdt = round((now - prev),2)

        dhdt_test = math.sqrt(math.pow(dhdt, 2))
        if dhdt_test > DHDT_THRESHOLD:
            dhdt = 0

        date = objectlist[i].posixdate
        dp = DP_Publish(date, dhdt)
        returnlist.append(dp)
    return returnlist

# ##################################################
# add storm data to dH / dt
# ##################################################
def storm_threshold(dhdtlist):
    returnlist = dhdtlist
    return returnlist

# ##################################################
# add aurora sightings to dH / dt
# ##################################################
def aurora_sightings(dhdtlist):
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

    # convert list to list of objects
    convertedlist = []
    for i in range(0, len(filtered_datalist)):
        datasplit = filtered_datalist[i].split(",")
        datetime = datasplit[0]
        datavalue = datasplit[1]
        dp = DP_Initial(datetime,datavalue)
        convertedlist.append(dp)


    print("Adding data to list of datetime bins")
    # Convert the list to binned data.
    binneddataobjects = create_bins(convertedlist)

    print("Converting the magnetic data to dH/dt")
    # Convert the objects in the list so we can process them
    dhdt_list = []
    for item in binneddataobjects:
        datetime = item.posixdate
        datavalue = item.average_datalist()
        dp = DP_Publish(datetime, datavalue)
        dhdt_list.append(dp)

    # # calculate the actual dH / dt. We will use the DP_Publish class now, so we can add storm threshholds and
    # # aurora sighting info.
    dhdt_list = create_dhdt(dhdt_list)

    # # Append the Aurora and Storm threshold info
    # dhdt_list = storm_threshold(dhdt_list)
    # dhdt_list = aurora_sightings(dhdt_list)

    # Save out data

    save_csv(binneddataobjects, "tg_magnetogram.csv")
    save_csv(dhdt_list, "tg_dhdt.csv")

    print("FINISHED")