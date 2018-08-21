#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 13:05:05 2018

@author: vaughn
"""
import re
from datetime import datetime
from time import mktime, time
import os

BIN_SIZE = 60 * 60 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total

class DPsimple:
    def __init__ (self, posixdate, datavalue):
        self.posixdate = posixdate
        self.datavalue = datavalue
        
    def print_values(self):
        return str(self.posixdate) + "," + str(self.datavalue)

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

    def minmax_datalist(self):
        temp = sorted(self.datalist)
        if len(temp) > 0:
            rangevalue = float(temp[len(temp)-1]) - float(temp[0])
        else:
            rangevalue = 0
        return rangevalue

    def print_values(self):
        returnstring = str(self.posixdate) + "," + str(self.minmax_datalist())
        return returnstring

def utc_to_posix(utcdate, formatstring):
    newdatetime = datetime.strptime(utcdate, formatstring)
    newdatetime = mktime(newdatetime.timetuple())
    newdatetime = int(newdatetime)
    return newdatetime






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
                newdata = input_array[i-j].datavalue
                datavalue = float(datavalue) + float(newdata)

            datavalue = round((datavalue / averaging_interval), 3)
            appendvalue = DPsimple(datetime, datavalue)
            displayarray.append(appendvalue)
            # print("Smoothing: "+ str(i) + " / " + str(len(input_array)))
    return displayarray




# ##################################################
# Binning - this is essentially a hash function based
# on the posix datetime
# ##################################################
def create_bins(objectlist):
    date_now = int(time())

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
        bin_id = int(round(bin_id, 0))
        binned_data[bin_id].datalist.append(objectlist[i].datavalue)
    return binned_data


class Station:
    def __init__(self, data_source, station_name, regex_time, dateformat):
        self.stationname = station_name
        self.datasource = data_source
        self.regex = regex_time
        self.dateformat = dateformat

    def get_raw_data(self, CSVlist):
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
        return rawdatalist

    # Use Object list
    def dhdt(self, objectlist):
        returnlist = []
        for i in range(1, len(objectlist)):
            datetime = objectlist[i].posixdate
            datavalue = float(objectlist[i].datavalue) - float(objectlist[i - 1].datavalue)
            dp = DPsimple(datetime, datavalue)
            returnlist.append(dp)
        return returnlist

    # Use CSV list
    def check_valid_utc(self, raw_csv_list, regex):
        returnlist = []
        errorcount = 0
        for item in raw_csv_list:
            itemsplit = item.split(",")
            utcdate = itemsplit[0]

            if re.match(regex, utcdate):
                returnlist.append(item)
            else:
                errorcount = errorcount + 1
        print(str(errorcount) + " errors in datetime encountered")
        return returnlist

    # Use CSV. Return [utc_date, data] only
    def clean_csv_data(self, raw_csv_list):
        returnlist = []
        # Ignore the first line as it should contain the header
        for i in range(1, len(raw_csv_list)):
            datasplit = raw_csv_list[i].split(",")
            datavalue = datasplit[1]
            datetime = datasplit[0]
            dp = datetime + "," + datavalue
            returnlist.append(dp)
        return returnlist

    # Use CSV data
    def medianfilter(self, datalist):
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

    # Use an object list
    def running_average(self, input_array, averaging_interval):
        displayarray = []
        if len(input_array) > averaging_interval:
            for i in range(averaging_interval + 1, len(input_array)):
                datavalue = 0
                datetime = input_array[i].posixdate
                for j in range(0, averaging_interval):
                    newdata = input_array[i - j].datavalue
                    datavalue = float(datavalue) + float(newdata)

                datavalue = round((datavalue / averaging_interval), 3)
                appendvalue = DPsimple(datetime, datavalue)
                displayarray.append(appendvalue)
        return displayarray

    # pass in CSV list
    def create_object_list(self, clean_csv, formatstring):
        return_object_list = []
        for item in clean_csv:
            datasplit = item.split(",")
            datetime = datasplit[0]
            datavalue = datasplit[1]
            posixvalue = utc_to_posix(datetime, formatstring)
            dp = DPsimple(posixvalue, datavalue)
            return_object_list.append(dp)
        return return_object_list

    # use an object list
    def save_csv(self, arraydata, savefile):
        try:
            os.remove(savefile)
        except:
            print("Error deleting old file")

        for item in arraydata:
            try:
                with open(savefile, 'a') as f:
                    f.write(item.print_values() + "\n")
            except IOError:
                print("WARNING: There was a problem saving your data")

    # Wrapper function to process data in an orderly fashion!
    def process_data(self):
        raw_data = self.get_raw_data(self.datasource)
        clean_data = self.check_valid_utc(raw_data, self.regex)
        clean_data = self.clean_csv_data(clean_data)
        clean_data = self.medianfilter(clean_data)
        clean_objects = self.create_object_list(clean_data, self.dateformat)
        self.save_csv(clean_objects, "data.csv")


if __name__ == "__main__":
    stationlist = []
    station1 = Station("teststation", "files.txt", "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d", "%Y-%m-%d %H:%M:%S.%f")
    stationlist.append(station1)

    for station in stationlist:
        station.process_data()


