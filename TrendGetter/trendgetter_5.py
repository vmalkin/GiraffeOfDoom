import os
import time
from datetime import datetime
from time import mktime
import re

BIN_SIZE = 60 * 60 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total

class Datapoint():
    def __init__(self, utc_date, datavalue):
        self.utc_date = utc_date
        self.datavalue = datavalue
        self.aurora_sighting = ""
        self.storm_threshold = ""

    def utc_2_posix(self):
        # set date time format for strptime()
        dateformat = "%Y-%m-%d %H:%M:%S.%f"
        newdatetime = datetime.strptime(self.utc_date, dateformat)
        # convert to Unix time (Seconds)
        newdatetime = mktime(newdatetime.timetuple())
        newdatetime = int(newdatetime)

        return newdatetime

    def print_values(self):
        returnstring = str(self.utc_date) + "," + str(self.datavalue)
        return returnstring

class DataBin():
    def __init__(self, posix_date):
        self.posix_date = posix_date
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

    def posix_2_utc(self):
        utctime = time.gmtime(int(float(self.posix_date)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        return utctime

    def print_values(self):
        returnstring = str(self.posix_date) + "," + str(self.average_datalist())
        return returnstring

# ##################################################
# Binning - this is essentially a hash function based
# on the posix datetime
# ##################################################
def create_bins(objectlist):
    # we do NOT want decimal values for time, only ints
    date_now = int(time.time())
    date_start = date_now - 31536000

    binned_data = []
    for i in range(date_start, date_now, BIN_SIZE):
        dp = DataBin(i)
        binned_data.append(dp)

    # THis is the hashing function to drop data into the correct bins
    # according to the date.
    for i in range(0, len(objectlist)):
        bin_id = (date_start - objectlist[i].utc_2_posix()) / BIN_SIZE
        bin_id = int(round(bin_id,0))
        binned_data[bin_id].datalist.append(objectlist[i].datavalue)

    return binned_data

# ##################################################
# median filter
# ##################################################
def medianfilter(arraylist):
    filteredlist = []
    for i in range(1,len(arraylist) - 1):
        templist = []
        templist.append(arraylist[i-1])
        templist.append(arraylist[i])
        templist.append(arraylist[i + 1])

        sortedlist = sorted(templist, key=lambda datastring: datastring[0])

        filteredlist.append(sortedlist[1])
    return filteredlist


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
# S C R I P T   B E G I N S   H E R E
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
    regex = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d)'
    rawdataobjects = []
    errorcount = 0
    for item in rawdatalist:
        itemsplit = item.split(",")
        utcdate = itemsplit[0]
        datavalue = itemsplit[1]

        if re.match(regex, utcdate):
            dp = Datapoint(utcdate, datavalue)
            rawdataobjects.append(dp)
        else:
            errorcount = errorcount + 1
    print(str(errorcount) + " errors in datetime encountered")

    # Convert the list to binned data.
    binneddataobjects = create_bins(rawdataobjects)
    save_csv(binneddataobjects, "tg_magnetogram.csv")

    current_dhdt = []
    # convert readings to dh/dt
    for i in range(1, len(binneddataobjects)):
        date_now = binneddataobjects[i].posix_date
        data_current = binneddataobjects[i].average_datalist()
        data_prev = binneddataobjects[i-1].average_datalist()
        data = (float(data_current) - float(data_prev))

        dp = Datapoint(date_now, data)
        current_dhdt.append(dp)

    save_csv(current_dhdt, "tg_diffs.csv")


    # Append the Aurora and Storm threshold info