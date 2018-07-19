import os
import time
from datetime import datetime
from time import mktime
import re
import math

BIN_SIZE = 60 * 10 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total
STORM_THRESHOLD = 14
aurora_sightings_list = "sightings.csv"

# A plain datapoint
class DPPlain():
    def __init__(self, posixdate, data):
        self.posixdate = posixdate
        self.data = data

    # allow an object to return it's values
    def print_values(self):
        values = str(self.posixdate) + "," + str(self.data)
        return values

# A bin object, used to collate data that falls in the same datetime
class Bin():
    """DataBin - This objects allows us to crate a bin of values.
    Calculates the average value of the bin"""
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

# Object used to create the final aggregated list
class DPPublish():
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


def initial_list_parse(rawdatalist):
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
            initial_datalist.append(dp)
        else:
            errorcount = errorcount + 1
    print(str(errorcount) + " errors in datetime encountered")
    return initial_datalist


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


# ##################################################
# Convert the list to dh/dt
# ##################################################
def create_dhdt(object_list):
    returnlist = []
    dhdt_threshold = 5
    for i in range(1, len(object_list)):
#        prevsplit = filtered_datalist[i-1].split(",")
#        nowsplit = filtered_datalist[i].split(",")

#        prev_data = float(prevsplit[1])
#        now_data = float(nowsplit[1])
#        now_datetime = nowsplit[0]
        prev_data = object_list[i-1].average_datalist()
        now_data = object_list[i].average_datalist()
        now_datetime = object_list[i].posixdate

        dhdt = float(now_data) - float(prev_data)
        if math.sqrt(math.pow(dhdt, 2)) > dhdt_threshold:
            dhdt = 0

        dp = DPPlain(now_datetime, dhdt)
        returnlist.append(dp)
    return returnlist


# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
# Data format is a list of DP_Plain objects
# #################################################################################
def running_average(input_array, averaging_interval):
    displayarray = []
    if len(input_array) > averaging_interval:
        for i in range(averaging_interval + 1, len(input_array)):
            datavalue = 0
            datetime = input_array[i].posixdate
            for j in range(0, averaging_interval):
                newdata = input_array[i-j].data
                datavalue = float(datavalue) + float(newdata)

            datavalue = round((datavalue / averaging_interval), 3)
            appendvalue = DPPlain(datetime, datavalue)
            displayarray.append(appendvalue)
            print("Smoothing: "+ str(i) + " / " + str(len(input_array)))
    return displayarray


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
        dp = Bin(i)
        binned_data.append(dp)

    # THis is the hashing function to drop data into the correct bins
    # according to the date.
    for i in range(0, len(objectlist)):
        bin_id = (float(objectlist[i].posixdate) - float(date_start)) / BIN_SIZE
        bin_id = int(round(bin_id,0))
        binned_data[bin_id].datalist.append(objectlist[i].data)
    return binned_data

def convert_to_obj(list):
    returnlist = []
    for item in list:
        datasplit = item.split(",")
        date = datasplit[0]
        data = datasplit[1]
        dp = DPPlain(date, data)
        returnlist.append(dp)
    return returnlist

# ##################################################
#
# S C R I P T   B E G I N S   H E R E
#
# ##################################################
# using the list of files, open each logfile into the main array
if __name__ == "__main__":
    # calculate the processing time
    starttime = time.time()

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
                    if firstline is True:
                        # print("Header identified, skipping...")
                        firstline = False
                    else:
                        line = line.strip()  # remove any trailing whitespace chars like CR and NL
                        rawdatalist.append(line)

        except IOError:
            print("A logfile appears to be present, but cannot be accessed at this time. ")

    # Convert the inital raw data to [posix_date, data] format
    magnetometer_data = initial_list_parse(rawdatalist)

    # Median filter out the blips
    magnetometer_data = medianfilter(magnetometer_data)
    
    # Convert the list to objects
    magnetometer_data = convert_to_obj(magnetometer_data)

    # Create the list of one-hour bins. Use a bin object that will allow us to hash on the posix dates
    magnetometer_data = create_bins(magnetometer_data)
    save_csv(magnetometer_data, "tg_rawmagdata.csv")

    # Convert the data to dH/dt.
    dhdt_objects = create_dhdt(magnetometer_data)

    # Smooth the dhdt data
    window = 40
    dhdt_objects = running_average(dhdt_objects, window)
    dhdt_objects = running_average(dhdt_objects, window)

    # # Add the Storm Threshold and Aurora Sighting data
    #
    # # Save the data out as a CSV file for display in highcharts
    save_csv(dhdt_objects, "tg_objects.csv")

    finishtime = time.time()
    elapsed = str(round((finishtime - starttime), 1))
    print("\nFinished. Time to process: " + elapsed + " seconds")

