import time

import standard_stuff as k
from os import path
from statistics import median, mean
import re


# Index positions of UTC date and data in each logfile. This could be different...
index_utcdate = 0
index_data = 1
regex_filename = "\d\d\d\d-\d\d-\d\d.csv"
rounding_value = 5


# Create a bin object. A bin:
# Covers a time period
# Has a list of data values for the time period
# Identifies if there was a magnetic storm for the time period
# Identifies if there were sightings recorded for the time period
# Can output time and data values as CSV formatted string.
# Can return a CSV formatted header for data
class Bin:
    def __init__(self, time):
        self.storm_threshhold = 4
        self.time = time
        self.data = []
        self.sighting = 0

    def dhdt(self):
        if len(self.data) > 0:
            value = round((max(self.data) - min(self.data)), rounding_value)
        else:
            value = 0
        return value

    def storm_detected(self):
        if self.dhdt() >= self.storm_threshhold:
            return 1
        else:
            return 0


def median_filter(list_to_parse):
    # Each element in the list has the format [datetime, data]
    returnlist = []
    for i in range(1, len(list_to_parse) - 1):
        t = []
        t.append(list_to_parse[i - 1][1])
        t.append(list_to_parse[i][1])
        t.append(list_to_parse[i + 1][1])
        medvalue = round(median(t), rounding_value)
        dt = list_to_parse[i][0]
        # the new datetime and median values
        newdp = [dt, medvalue]
        returnlist.append(newdp)
    return returnlist


def h_to_dhdt(array_time_data):
    returnlist = []
    for i in range(1, len(array_time_data)):
        tt = array_time_data[i][0]
        dh = array_time_data[i][1] - array_time_data[i - 1][1]
        dh = round(dh, rounding_value)
        dp = [tt, dh]
        returnlist.append(dp)
    return returnlist


def smooth_data(array_time_data):
    # Each element in the list has the format [datetime, data]
    # The half window value should cover 10 minutes of data
    returnlist = []
    halfwindow = 10 * 4
    for i in range(halfwindow, len(array_time_data) - halfwindow):
        d = []
        for j in range(0 - halfwindow, halfwindow):
            if j == 0:
                tt = array_time_data[i + j][0]
            d.append(array_time_data[i + j][1])
        dd = mean(d)
        dp = [tt, dd]
        returnlist.append(dp)
    return returnlist


if __name__ == '__main__':
    regex_data = "[0-9][.][0-9]"
    array_time_data = []

    # does files.txt exist? if not, abort
    if path.exists(k.file_list):
        # load files.txt
        with open(k.file_list, "r") as filelist:
            for filename in filelist:
                nw_filename = filename.strip()
                if re.match(regex_filename, nw_filename):
                    # open each file in the list
                    # parse thru each file, extract date and data value. If valid assemble into master list
                    with open(nw_filename, "r") as csvdata:
                        for csvline in csvdata:
                            newcsv = csvline.strip()
                            newcsv = newcsv.split(",")
                            # If we have data and not a header
                            if re.match(regex_data, newcsv[index_data]):
                                posixtime = k.utc2posix(newcsv[0], "%Y-%m-%d %H:%M:%S.%f")
                                data = float(newcsv[index_data])
                                dp = [posixtime, data]
                                array_time_data.append(dp)

        # Remove any spikes in data with a median filter.
        array_time_data = median_filter(array_time_data)

        # smooth the data
        array_time_data = smooth_data(array_time_data)

        # Convert the data into dh/dt
        array_time_data = h_to_dhdt(array_time_data)

        # Create a series of 365 dated bins for the previous 365 days
        nowdate = int(time.time())
        startdate = nowdate - 86400 * 365

        array_year = []
        for i in range(365, 0, -1):
            d = nowdate - i * 86400
            array_year.append(Bin(d))

        # parse thru the list and allocate data values to bins (each bin will have a list of data for the day)
        for item in array_time_data:
            tt = item[0]
            dd = item[1]
            index = int((tt - startdate) / 86400)
            if index >= 0:
                if index < 365:
                    array_year[index].data.append(dd)

        # open the sightings file. allocate the dates of sightings to each bin.
        with open("sightings.csv", "r") as s:
            for line in s:
                t = line.strip()
                tt = k.utc2posix(t, "%d/%m/%Y")
                index = int((tt - startdate) / 86400)
                if index >= 0:
                    if index < 365:
                        array_year[index].sighting = 1

        for item in array_year:
            print(item.time, item.dhdt(), item.storm_detected(), item.sighting)

    else:
        print("FILES.TXT does not exists. Create list of log files then rerun this script.")
