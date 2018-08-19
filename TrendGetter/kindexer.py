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


def get_csv_data():
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
    return rawdatalist

# parse thru list and return [utc_date, data] only
def clean_csv_data(raw_csv_list):
    returnlist = []
    # Ignore the first line as it should contain the header
    for i in range(1, len(raw_csv_list)):
        datasplit = raw_csv_list[i].split(",")
        datavalue = datasplit[1]
        datetime = datasplit[0]
        dp = datetime + "," + datavalue
        returnlist.append(dp)
    return returnlist

def check_valid_utc(raw_csv_list, regex, dateformat):
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
    
def utc_to_posix(utcdate, formatstring):
    newdatetime = datetime.strptime(utcdate, formatstring)
    newdatetime = mktime(newdatetime.timetuple())
    newdatetime = int(newdatetime)
    return newdatetime

def create_object_list(clean_csv, formatstring): 
    return_object_list = []    
    for item in clean_csv:
        datasplit = item.split(",")
        datetime = datasplit[0]
        datavalue = datasplit[1]
        posixvalue = utc_to_posix(datetime, formatstring)
        dp = DPsimple(posixvalue, datavalue)
        return_object_list.append(dp)
    return return_object_list

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

def dhdt(objectlist):
    returnlist = []
    for i in range(1, len(objectlist)):
        datetime = objectlist[i].posixdate
        datavalue = float(objectlist[i].datavalue) - float(objectlist[i-1].datavalue)
        dp = DPsimple(datetime, datavalue)
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
                newdata = input_array[i-j].datavalue
                datavalue = float(datavalue) + float(newdata)

            datavalue = round((datavalue / averaging_interval), 3)
            appendvalue = DPsimple(datetime, datavalue)
            displayarray.append(appendvalue)
            # print("Smoothing: "+ str(i) + " / " + str(len(input_array)))
    return displayarray

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


if __name__ == "__main__":
    # this could run on a while loop
    regex = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d)'
    dateformat = "%Y-%m-%d %H:%M:%S.%f"
    raw_csv_list = get_csv_data()
    
    # clean the data up
    clean_data = check_valid_utc(raw_csv_list, regex, dateformat)
    clean_data = clean_csv_data(clean_data)
    clean_data = medianfilter(clean_data)
   
    # Create the object list
    object_list = create_object_list(clean_data, dateformat)
    dhdt_list = object_list

    # Convert to dH/dt, then smooth.
    dhdt_list = dhdt(object_list)
    dhdt_list = running_average(dhdt_list, 30)
    dhdt_list = running_average(dhdt_list, 30)
    save_csv(dhdt_list, "dhdt.csv")

    binned_objects = create_bins(dhdt_list)

    save_csv(binned_objects, "magnetogram.csv")
    # Bin according to user preference and calc the range of the bin values
    print("Finished")
