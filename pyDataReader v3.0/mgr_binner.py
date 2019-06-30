import time
import math
import logging
import os
import sys
import constants as k

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)


class BinData():
    def __init__(self, field_correction):
        self.posix_time = 0
        self.data_values = []
        self._flipvalue = field_correction

    def average_value(self):
        avg = 0.0
        if len(self.data_values) > 0:
            for item in self.data_values:
                avg = avg + float(item)
            avg = avg / float(len(self.data_values))
        if avg == 0:
            avg = ""
        return avg

    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posix_time)))
        utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
        return utctime

    def print_values(self):
        value_string = (str(self._posix2utc()) + "," + str(self.average_value() * self._flipvalue))
        return value_string




class Binner():
    """
    The binner is designed to take an array of data in the format [posix_datestamp, datavalue] and convert the
    interval of the timestamp. Eg. if the data is recorded every 2 seconds, Binner can convert the data to readings
    at one minute, or 20 minute intervals instead.
    """
    def __init__(self, raw_data_array, timespan, binsize, field_correction):
        self._raw_data_array = raw_data_array
        self._timespan = timespan
        self._binsize = binsize
        self._fieldcorrection = field_correction

    def processbins(self):
        t_now = int(time.time())
        t_start = int(t_now - self._timespan)

        # set up the list of bins
        final_data_bins = []

        # Add the timestamps to the bin list
        for i in range(t_start, t_now, self._binsize):
            dp = BinData(self._fieldcorrection)
            dp.posix_time = i
            final_data_bins.append(dp)

        # parse thru the raw data, identifying datapoints that fall within the bins
        # and adding their data to each bins internal array of data.
        # each item is a type of DataPoint - see DataPoint.py
        for item in self._raw_data_array:
            itemdata = round(float(item.data_1), 4)
            itemtime = item.posix_time
            if float(itemtime) >= float(t_start):
                index = math.floor((float(itemtime) - float(t_start)) / float(self._binsize))
                final_data_bins[index].data_values.append(itemdata)

        savefile = k.publish_folder + "/" + k.station_id + "_1minbins.csv"
        # get each BinDatapoint to spit out the avg of it's stored data, as well as the UTC time.
        try:
            os.remove(savefile)
        except OSError:
            print("WARNING: could not delete " + savefile)
            logging.warning("WARNING: File IO Exception raised - could not delete: " + savefile)

        for i in range(0, len(final_data_bins)):
            with open(savefile, "a") as s:
                try:
                    s.write(final_data_bins[i].print_values() + "\n")
                except:
                    print(sys.exc_info())
                    
        # We just want the last minutes reading for Brendan
        savefile = "brendan.csv"
        try:
            os.remove(savefile)
        except OSError:
            print("WARNING: could not delete " + savefile)
            logging.warning("WARNING: File IO Exception raised - could not delete: " + savefile)

        # get each BinDatapoint to spit out the avg of it's stored data, as well as the UTC time.
        with open(savefile, "w") as s:
            try:
                s.write(final_data_bins[len(final_data_bins) - 1].print_values() + "\n")
            except:
                print(sys.exc_info())
