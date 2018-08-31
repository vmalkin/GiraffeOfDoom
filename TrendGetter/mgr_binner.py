#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 13:05:05 2018

@author: vaughn
"""
import re
from datetime import datetime
import time
import os
import math

BIN_SIZE = 60 * 60# the number of seconds wide a bin is
DURATION = 60*60*24
BIN_NUMBER = int(DURATION / BIN_SIZE)  # how many bins we want in total
STORMTHRESHOLD = 0.25

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
        rangevalue = round(rangevalue, 5)
        return rangevalue

    def posix2utc(self):
        utctime = time.gmtime(int(float(self.posixdate)))
        utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
        return utctime

    def print_values(self):
#        returnstring = str(self.posix2utc()) + "," + str(self.minmax_datalist()) + "," + str(self.stormthreshold) + "," + str(self.aurorasighting)
        returnstring = str(self.posix2utc()) + "," + str(self.minmax_datalist())
        return returnstring


class Station:
    def __init__(self, station_name, data_source,  regex_time, dateformat):
        self.stationname = station_name
        self.datasource = data_source
        self.regex = regex_time
        self.dateformat = dateformat

    # this function will need to be customised accordingly
    def get_raw_data(self, csvdatafile):
        rawdatalist = []
        
        firstline = True
        try:
            with open(csvdatafile) as e:
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

    def utc_to_posix(self, utcdate, formatstring):
        newdatetime = datetime.strptime(utcdate, formatstring)
        newdatetime = time.mktime(newdatetime.timetuple())
        newdatetime = int(newdatetime)
        return newdatetime

    # Use Object list
    def dhdt(self, objectlist):
        returnlist = []
        BLIP = float(3)
        for i in range(1, len(objectlist)):
            datetime = objectlist[i].posixdate
            datavalue = float(objectlist[i].datavalue) - float(objectlist[i - 1].datavalue)
            if math.sqrt(math.pow(datavalue,2)) > BLIP:
                print("Blip!")
                datavalue = 0
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
        print("Smoothing data")
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
            posixvalue = datetime
#            posixvalue = self.utc_to_posix(datetime, formatstring)
            dp = DPsimple(posixvalue, datavalue)
            return_object_list.append(dp)
        return return_object_list

    # use an object list
    def save_csv(self, arraydata, savefile):
        print("Saving file " + savefile)
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

    def create_bins(self, objectlist):
        date_now = int(time.time())
#        date_now = 1535322670
        date_start = date_now - DURATION

        binned_data = []
        for i in range(date_start, date_now, BIN_SIZE):
            dp = Bin(i)
            binned_data.append(dp)

        # THis is the hashing function to drop data into the correct bins
        # according to the date.
        for i in range(0, len(objectlist)):  
            bin_id = (float(objectlist[i].posixdate) - float(date_start)) / BIN_SIZE
            bin_id = int(round(bin_id, 0))
            if bin_id >= 0 and bin_id < BIN_NUMBER:         
                binned_data[bin_id].datalist.append(objectlist[i].datavalue)
        return binned_data

    # Wrapper function to process data in an orderly fashion!
    def process_data(self):
        raw_data = self.get_raw_data(self.datasource)
#        clean_data = self.check_valid_utc(raw_data, self.regex)
        clean_data = self.clean_csv_data(raw_data)
        clean_data = self.medianfilter(clean_data)
        clean_objects = self.create_object_list(clean_data, self.dateformat)
        clean_objects = self.dhdt(clean_objects)
        clean_objects = self.running_average(clean_objects, 20)
        clean_objects = self.running_average(clean_objects, 20)
#        self.save_csv(clean_objects, "dhdt.csv")
        clean_objects = self.create_bins(clean_objects)
        self.save_csv(clean_objects, self.stationname+".csv")


if __name__ == "__main__":
    starttime = time.time()
    stationlist = []
    station1 = Station("kindex", "arraysave.csv", "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d", "%Y-%m-%d %H:%M:%S.%f")
    stationlist.append(station1)

    for station in stationlist:
        station.process_data()

    finishtime = time.time()
    elapsed = str(round((finishtime - starttime), 1))
    print("\nFinished. Time to process: " + elapsed + " seconds")
