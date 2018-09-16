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

BIN_SIZE = 60 * 60 *2 # the number of seconds wide a bin is
DURATION = 60*60*24*365
BIN_NUMBER = int(DURATION / BIN_SIZE)  # how many bins we want in total
STORMTHRESHOLD = 0.25   # geomagnetic activity over this number constitutes a storm
CSV_SPLITLENGTH = 3   # The number of CSV elements in a line from our source data.
CSV_UTCPOSITION = 0
CSV_POSIXPOSITION = 1
CSV_DATAPOSITION = 2

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

    def print_values(self):
        returnstring = str(self.posix2utc()) + "," + str(self.minmax_datalist()) + "," + str(self.stormthreshold) + "," + str(self.aurorasighting)
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


    def utc_to_posix(self,datalist, formatstring):
        returnlist = []
        for item in datalist:
            datasplit = item.split(",")
            utcdate = datasplit[0]
            data = datasplit[1]
            newdatetime = datetime.strptime(utcdate, formatstring)
            newdatetime = time.mktime(newdatetime.timetuple())
            newdatetime = int(newdatetime)
            dp = newdatetime + "," + data
            returnlist.append(dp)
        return returnlist
		
	def posix_to_utc(self,datalist, formatstring):
		pass

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

    # parse raw data for only UTC and data values
    def get_utc_data(self, raw_data):
        returnlist = []
        for item in raw_data:
            datasplit = item.split(",")
            utctime = datasplit[CSV_UTCPOSITION]
            data = datasplit[CSV_DATAPOSITION]
            dp = utctime + "," + data
            returnlist.append(dp)
        return returnlist

    # # data is in format [utcdate, datavalue]
    # def utc_to_posix(self, utc_data, formatstring):
    #     returnlist = []
    #     for item in utc_data:
    #         datasplit = item.split(",")
    #         posixvalue = self.utc_to_posix(datasplit[0], formatstring)
    #         datavalue = datasplit[1]
    #         dp = posixvalue + "," + datavalue
    #         returnlist.append(dp)
    #     return returnlist

    #
    # # Use CSV. Return [utc_date, data] only
    # # Here is where we need to adjust which values are date and data
    # def clean_csv_data(self, raw_csv_list):
    #     returnlist = []
    #     # Ignore the first line as it should contain the header
    #     for i in range(1, len(raw_csv_list)):
    #         datasplit = raw_csv_list[i].split(",")
    #         if len(datasplit) == CSV_SPLITLENGTH:
    #             datavalue = datasplit[2]
    #             datetime = datasplit[1]
    #             dp = datetime + "," + datavalue
    #             returnlist.append(dp)
    #     return returnlist

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

        for item in arraydata:
            try:
                with open(savefile, 'a') as f:
                    f.write(item.print_values() + "\n")
            except IOError:
                print("WARNING: There was a problem saving your data")


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
            bin_id = int(round(bin_id, 0))
            binned_data[bin_id].datalist.append(objectlist[i].datavalue)
        return binned_data
		
	# If yyyy-mm-dd of the posix storm date equals yyyy-mm-dd of the object date
	# then set the aurora sightings value of the object
    # def set_aurorasighting(self, object_list, date_list_file):
    #     posixdates = []
    #     with open(date_list_file) as e:
    #         for line in e:
    #             date = line.strip()  # remove any trailing whitespace chars like CR and NL
    #             dt = utc_2_unix(date)
    #             posixdates.append(dt)

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
        #Parse thru with a median filter too!
        clean_data = self.check_valid_utc(raw_data, self.regex)
        clean_data = self.medianfilter(clean_data)

        # Convert list to [posix, data]
        clean_data = self.utc_to_posix(clean_data)

        # Convert list to object_list




        # get data into format of UTC, Data


        # clean_data = self.clean_csv_data(raw_data)

        # clean_data = self.utc_to_posix(clean_data, self.dateformat)


        clean_objects = self.create_object_list(clean_data)
        clean_objects = self.dhdt(clean_objects)
        # self.save_csv(clean_objects, "dhdt.csv")
        clean_objects = self.running_average(clean_objects, 20)
        clean_objects = self.running_average(clean_objects, 20)
        clean_objects = self.create_bins(clean_objects)
        # <<--SNIP-->>
        # self.set_aurorasighting(clean_objects, "sightings.csv")
        self.set_stormthreshold(clean_objects)
        # <<--SNIP-->>
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
