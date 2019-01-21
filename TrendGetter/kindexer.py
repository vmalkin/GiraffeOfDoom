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

BIN_SIZE = 60 * 60 # the number of seconds wide a bin is
DURATION = 60*60*24
CARRINGTON_ROTATION = int(60*60*24*27.2753)
BIN_NUMBER = int(DURATION / BIN_SIZE)  # how many bins we want in total
STORMTHRESHOLD = 0.25   # geomagnetic activity over this number constitutes a storm
CSV_SPLITLENGTH = 4   # The number of CSV elements in a line from our source data.
CSV_UTCPOSITION = 0
CSV_POSIXPOSITION = 0
CSV_DATAPOSITION = 1
BLIP = float(50000)

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
        # <<--SNIP-->>
        self.aurorasighting = ""
        self.stormthreshold = ""
        self.carrington_rotation = ""
        # <<--SNIP-->>

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

    def print_csv_header(self):
        returnstring = "Date/Time(UTC), Geomagnetic Activity, Storm Detected, Aurora Sighted, Carrington Rotation Marker"
        return returnstring

    # def print_csv_header(self):
    #     returnstring = "Date/Time(UTC), Geomagnetic Activity"
    #     return returnstring

    def print_values(self):
        returnstring = str(self.posix2utc()) + "," + str(self.minmax_datalist()) + "," + str(self.stormthreshold) + "," + str(self.aurorasighting) + "," + str(self.carrington_rotation)
        return returnstring



# ##################################################
# Binning - this is essentially a hash function based
# on the posix datetime
# ##################################################



class Station:
    def __init__(self, station_name, data_source,  regex_time, dateformat):
        self.stationname = station_name
        self.datasource = data_source
        self.regex = regex_time
        self.dateformat = dateformat

    # def get_raw_data(self, posixlist):
    #     return posixlist

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


    def utc_to_posix(self, utcdate, formatstring):
        posixtime = datetime.strptime(utcdate, formatstring)
        posixtime = time.mktime(posixtime.timetuple())
        return str(int(posixtime))

    def posix_to_utc(self, posix_date, formatstring):
        utcstring = datetime.utcfromtimestamp(posix_date).strftime(formatstring)
        return utcstring


    # Use Object list
    def dhdt(self, objectlist):
        returnlist = []
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

    # parse raw data for only UTC and data values
    def get_utc_data(self, raw_data):
        returnlist = []
        for item in raw_data:
            datasplit = item.split(",")
            if len(datasplit) == CSV_SPLITLENGTH:
                utctime = datasplit[CSV_UTCPOSITION]
                data = datasplit[CSV_DATAPOSITION]
                dp = utctime + "," + data
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
    def create_object_list(self, clean_csv):
        return_object_list = []
        for item in clean_csv:
            datasplit = item.split(",")
            datetime = datasplit[0]
            datavalue = datasplit[1]
            dp = DPsimple(datetime, datavalue)
            return_object_list.append(dp)
        return return_object_list

    # use an object list
    def save_csv(self, arraydata, savefile):
        print("Saving file " + savefile)
        try:
            os.remove(savefile)
        except:
            print("Error deleting old file")

        header = Bin(10)
        try:
            with open(savefile, 'a') as f:
                f.write(header.print_csv_header() + "\n")
        except IOError:
            print("WARNING: Unable to write header to CSV file")

        for item in arraydata:
            try:
                with open(savefile, 'a') as f:
                    f.write(item.print_values() + "\n")
            except IOError:
                print("WARNING: There was a problem saving your data")

    # uses a data list
    def convert_to_posix(self, clean_data):
        returnlist = []
        for item in clean_data:
            datasplit = item.split(",")
            posix_date = self.utc_to_posix(datasplit[0], self.dateformat)
            data = datasplit[1]
            dp = posix_date + "," + data
            returnlist.append(dp)
        return returnlist


    def create_bins(self, objectlist):
        date_now = int(time.time())
        date_start = date_now - DURATION

        binned_data = []
        for i in range(date_start, date_now, BIN_SIZE):
            dp = Bin(i)
            binned_data.append(dp)

        # THis is the hashing function to drop data into the correct bins
        # according to the date.
        for i in range(0, len(objectlist)):
            bin_id = (float(objectlist[i].posixdate) - float(date_start)) / BIN_SIZE
            bin_id = int(round(bin_id, 0))-1
            binned_data[bin_id].datalist.append(objectlist[i].datavalue)
        return binned_data
		
    # If yyyy-mm-dd of the posix storm date equals yyyy-mm-dd of the object date
    # then set the aurora sightings value of the object
    def set_aurorasighting(self, object_list, date_list_file):
        posixdates = []
        with open(date_list_file) as e:
            for line in e:
                date = line.strip()  # remove any trailing whitespace chars like CR and NL
                posix_date = self.utc_to_posix(date, "%d/%m/%Y")
                posixdates.append(posix_date)

        print("Iterating thru aurora sighting dates - this could take a while!")
        for auroradate in posixdates:
            one = (self.posix_to_utc(int(auroradate), "%Y-%m-%d"))
            for dataobject in object_list:
                tother = (self.posix_to_utc(int(dataobject.posixdate), "%Y-%m-%d"))
                if one == tother:
                    dataobject.aurorasighting = 0.2

    def set_carringtons(self, object_list):
        carrington_count = int(CARRINGTON_ROTATION / BIN_SIZE)
        for i in range(0, len(object_list), carrington_count):
            object_list[i].carrington_rotation = 0.04

    def set_stormthreshold(self, objectlist):
        for item in objectlist:
            range = item.minmax_datalist()
            if range >= STORMTHRESHOLD:
                # the datapoint is plotted at this position.
                item.stormthreshold = 0.02

    # designed to give
    def parse_startistics(self, objectlist):
        pass

    # Wrapper function to process data in an orderly fashion!
    def process_data(self):
        # Get the raw data
        raw_data = self.get_raw_data(self.datasource)

        # From raw data get [UTC, data] --> list
        raw_data = self.get_utc_data(raw_data)

        # Check UTC format. Reject malformed time values
        clean_data = self.check_valid_utc(raw_data, self.regex)

        # Parse thru with a median filter too!
        clean_data = self.medianfilter(raw_data)

        # Convert list to [posix, data]
        clean_data = self.convert_to_posix(clean_data)
        print(str(len(clean_data)))
        # Convert list to object_list
        clean_objects = self.create_object_list(clean_data)
        self.save_csv(clean_objects, "test.csv")
        clean_objects = self.dhdt(clean_objects)


        # self.save_csv(clean_objects, "dhdt.csv")
        clean_objects = self.running_average(clean_objects, 20)
        clean_objects = self.running_average(clean_objects, 20)
        clean_objects = self.create_bins(clean_objects)
        # # <<--SNIP-->>
        # self.set_aurorasighting(clean_objects, "sightings.csv")
        # self.set_stormthreshold(clean_objects)
        # self.set_carringtons(clean_objects)
        # # <<--SNIP-->>
        self.save_csv(clean_objects, self.stationname+".csv")

if __name__ == "__main__":
    starttime = time.time()
    stationlist = []
    station1 = Station("aurora_activity", "files.txt", "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d", "%Y-%m-%d %H:%M:%S.%f")
    stationlist.append(station1)

    for station in stationlist:
        station.process_data()

    finishtime = time.time()
    elapsed = str(round((finishtime - starttime), 1))
    print("\nFinished. Time to process: " + elapsed + " seconds")
