import constants as k
from datapoint import DataPoint
import math
import time
import logging

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

class BinDatapoint:
    """The datapoint used when binning data"""
    def __init__(self, posixtime):
        self.posix_time = posixtime
        self.datavalues = []

    # convert the internal posx_date to UTC format
    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posix_time)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        return utctime

    def return_average(self):
        returnvalue = float(0)
        if len(self.datavalues) > 0:
            for item in self.datavalues:
                returnvalue = returnvalue + float(item)
            returnvalue = round((returnvalue / len(self.datavalues)), 2)
        else:
            returnvalue = ""
        return returnvalue

    def print_values(self):
        returnstring = str(self._posix2utc()) + "," + str(self.return_average())
        return returnstring


class BinBinlist:
    """Sets up to bin data. Datalist uses the Datapoint class."""
    def __init__(self, binwidth, datalist, savefilename):
        self.savefilename = savefilename
        self.datalist = datalist
        self.binwidth = binwidth
        self._posix_end = int(math.floor(time.time()))
        self._posix_start = int(self._posix_end - (60 * 60 * 24))

        self.binlist = []
        for i in range(self._posix_start, self._posix_end + self.binwidth, self.binwidth):
            dp = BinDatapoint(i)
            self.binlist.append(dp)

    def _binlist_index(self, posixtime):
        index = math.floor((float(posixtime) - float(self._posix_start)) / self.binwidth)
        return index

    def process_datalist(self):
        for data in self.datalist:
            indexvalue = self._binlist_index(data.posix_time)
            if indexvalue >= 0:
                self.binlist[indexvalue].datavalues.append(data.data_1)

    def save_file(self):
        try:
            with open(self.savefilename, 'w') as w:
                for dataObjects in self.binlist:
                    w.write(dataObjects.print_values() + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + self.savefilename)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + self.savefilename)


def median_filter(datalist):
    """Simple median_filter filter - window sized fixed at 3 datapoints"""
    returnlist = datalist
    if len(datalist) > 10:
        returnlist = []
        for i in range(1, len(datalist) - 2):
            sortlist = []
            sortlist.append(float(datalist[i - 1].data_1))
            sortlist.append(float(datalist[i].data_1))
            sortlist.append(float(datalist[i + 1].data_1))
            sortlist.sort()
            data = sortlist[1]
            datetime = datalist[i].posix_time
            dp = DataPoint(datetime, data)
            returnlist.append(dp)
    return returnlist

def median_window_filter(datalist, half_window_size):
    """Median Filter w/flexible window size"""
    returnlist = []
    if len(datalist) > int(half_window_size):
        for i in range(half_window_size, len(datalist) - half_window_size):
            templist = []
            datetime = datalist[i].posix_time
            for j in range(half_window_size * -1 , half_window_size):
                # print(str(i) + " " + str(j))
                data = float(datalist[i+j].data_1)
                templist.append(data)
            templist.sort()
            data = templist[half_window_size]
            dp = DataPoint(datetime, data)
            returnlist.append(dp)
    return returnlist


def recursive_filter(datalist):
    """Recursive filter"""
    returnlist = datalist
    if len(datalist) > 2:
        returnlist = []
        prev_value = float(datalist[0].data_1)
        for i in range(1, len(datalist)):
            new_data_1 = (float(k.recursive_constant) * float(datalist[i].data_1)) + ((1 - k.recursive_constant) * prev_value)
            dp = DataPoint(datalist[i].posix_time, new_data_1)
            returnlist.append(dp)
            prev_value = new_data_1
    return returnlist




