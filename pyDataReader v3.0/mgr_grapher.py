import constants as k
from datapoint import DataPoint
import math
import time
import logging

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

class BinDatapoint:
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
            self.binlist[indexvalue].datavalues.append(data.data_1)

    def save_file(self):
        try:
            with open(self.savefilename, 'w') as w:
                for dataObjects in self.binlist:
                    w.write(dataObjects.print_values() + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + self.savefilename)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + self.savefilename)


def deblip(datalist):
    """Deblips data according to the blip value stored in constants.py"""
    workinglist = []
    primedata = datalist[0].data_1
    primedate = datalist[0].posix_time

    for i in range(1, len(datalist)):
        dhdt = float(datalist[i].data_1) - float(datalist[i-1].data_1)
        if math.sqrt(dhdt**2) >= k.noise_spike:
            dhdt = 0

        dp = DataPoint(datalist[i].posix_time, dhdt)
        workinglist.append(dp)

    returnlist = []
    dp = DataPoint(primedate, primedata)
    returnlist.append(dp)

    for magdata in workinglist:
        newdate = magdata.posix_time
        newdata = magdata.data_1 + float(returnlist[len(returnlist)-1].data_1)
        dp = DataPoint(newdate, newdata)
        returnlist.append(dp)
    return returnlist
