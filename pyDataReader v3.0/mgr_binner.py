import time
import math
import logging
import sys
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

'''
the datapoint to aggrgate binned values
This version of the binner creates an AVERAGE in each bin. THis can be modifed to find a max and min, hence
a rate of change. 
'''
class BinData():
    def __init__(self):
        self.posix_time = 0
        self.data_values = []

    def average_value(self):
        avg = 0.0
        if len(self.data_values) > 0:
            for item in self.data_values:
                avg = avg + float(item)
            avg = avg / float(len(self.data_values))
        return avg

    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posix_time)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        return utctime

    def print_values(self):
        value_string = (str(self._posix2utc()) + "," + str(self.average_value()))
        return value_string

class Binner():
    def __init__(self, raw_data_array, timespan, binsize):
        self._raw_data_array = raw_data_array
        self._timespan = timespan
        self._binsize = binsize
        self.binned_data = self._createbins()

    # setup the list of bins
    def _createbins(self):
        blankbins = []
        maxrange = int(self._timespan / self._binsize)
        for i in range(0,maxrange):
            dp = BinData()
            blankbins.append(dp)
        return blankbins

    # parse thru the raw data and drop each datapoint's value into the correct bin
    def create_binned_values(self):
        t_now = time.time()
        t_deduct = t_now - self._timespan

        # aggregate the data values into the correct bins
        for data in self._raw_data_array:
            bin_index = math.floor((float(data.posix_time) - float(t_deduct)) / float(self._binsize))
            self.binned_data[bin_index].data_values.append(data.data_1)


        # insert the timestamp for each bin
        for i in range(0, len(self.binned_data)):
            self.binned_data[i].posix_time = (i * self._binsize) + t_deduct

        filename = "graphing/RuruRapid.1minbins.csv"
        try:
            with open(filename, 'w') as w:
                for dataObjects in self.binned_data:
                    w.write(dataObjects.print_values() + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + filename)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + filename)

