import time
import datetime
import math
import logging
import os
import re
import sys
errorloglevel = logging.ERROR
logging.basicConfig(filename="errors_plotter.log", format='%(asctime)s %(message)s', level=errorloglevel)

__version__ = "3.0"
__author__ = "Vaughn Malkin"

BINNED_PRELIM_DATA = "DELETE_ME_to_recalculate.csv"
timespan = 31536000
binsize = 3600
t_now = int(time.time())
t_deduct = t_now - timespan

# #############################
# R A W D A T A P O I N T   C L A S S
# #############################
class RawDataPoint:
    def __init__(self, utc_time, data_1):
        self.utc_time = utc_time
        self.posix_time = self.utc2posix()
        self.binindex = self.binindexer()
        self.data_1 = data_1

    # calculates an index position for this data value in a list of binned data, based on the
    # POSIX timestamp
    def binindexer(self):
        bin_index = math.floor((float(self.posix_time) - float(t_deduct)) / float(binsize))
        return bin_index

    def utc2posix(self):
        dateformat = "%Y-%m-%d %H:%M:%S.%f"
        newdatetime = datetime.datetime.strptime(self.utc_time, dateformat)
        newdatetime = time.mktime(newdatetime.timetuple())
        return newdatetime

    # return the values of this datapoint as a string
    def print_values(self):
        printvalue = str(self.utc_time) + "," + str(self.data_1)
        return printvalue


'''
the datapoint to aggrgate binned values
This version of the binner creates an AVERAGE in each bin. THis can be modifed to find a max and min, hence
a rate of change. 
'''
class FinalBinDataPoint():
    def __init__(self):
        self.posix_time = 0
        self.data_values = []
        self.aurora_sighted = ""
        self.storm_present = ""

    # calculates the average value of the data stored in the data_values list
    def _average_value(self):
        avg = 0.0
        if len(self.data_values) > 0:
            for item in self.data_values:
                avg = avg + float(item)
            avg = avg / float(len(self.data_values))
            avg = round(avg, 3)
        if avg == 0:
            avg = ""
        return avg

    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posix_time)))
        utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
        return utctime

    def print_values(self):
        value_string = (str(self._posix2utc()) + "," + str(self._average_value()))
        return value_string


if __name__ == "__main__":
    starttime = time.time()
    rawdata = []

    CSVlist = "files.txt"
    CSVFilenames = []

    if not os.path.isfile(BINNED_PRELIM_DATA):
        logging.debug("Load in list of CSV data file names.")
        if os.path.isfile(CSVlist):
            try:
                with open(CSVlist) as e:
                    for line in e:
                        line = line.strip()  # remove any trailing whitespace chars like CR and NL
                        CSVFilenames.append(line)

            except IOError:
                logging.debug("List of logfiles appears to be present, but cannot be accessed at this time.")
                print("List of logfiles appears to be present, but cannot be accessed at this time. ")

        print("Adding logfile data...")

        rawdatalist = []
        # Parse thru the CSVfilelist, Append values to our raw data list
        for item in CSVFilenames:
            logging.debug("Begin parse of CSV data.")
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
                            linesplit = line.split(",")
                            utcdate = linesplit[0]
                            data = linesplit[1]

                            # if the datestring parses, create the datapoint
                            if re.match(r"\A\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{2}\Z",utcdate):
                                dp = RawDataPoint(utcdate, data)
                                rawdatalist.append(dp)
                            else:
                                logging.error("REGEX: regex on UTC time failed: " + str(line))
            except IOError:
                logging.debug("A logfile appears to be present, but cannot be accessed at this time. ")
                print("A logfile appears to be present, but cannot be accessed at this time. ")

        # set up the list of bins
        final_data_bins = []

        # Add the timestamps to the bin list
        for i in range(t_deduct, t_now, binsize):
            dp = FinalBinDataPoint()
            dp.posix_time = i
            final_data_bins.append(dp)

        # parse thru the raw data, identifying datapoints that fall within the bins
        # and adding their data to each bins internal array of data.
        for i in range(0, len(rawdatalist)):
            data = rawdatalist[i].data_1
            index = rawdatalist[i].binindex
            final_data_bins[index].data_values.append(data)

        print("Creating CSV data - please wait...")
        savefile = "test.csv"
        try:
            os.remove(savefile)
        except:
            print("Error deleting old file")

        # get each BinDatapoint to spit out the avg of it's stored data, as well as the UTC time.
        for i in range(0, len(final_data_bins)):
            with open(savefile, "a") as s:
                try:
                    # print(str(i) + " / " + str(len(final_data_bins)))
                    s.write(final_data_bins[i].print_values() + "\n")
                except:
                    pass


        t_fin = time.time()
        elapsed = (t_fin - t_now) / 60
        elapsed = round(elapsed,2)
        print("Time to process: " + str(elapsed) + " minutes")





