import constants as k
from datapoint import DataPoint
import math
import time

class Bin_Datapoint():
    def __init__(self, posixtime):
        self.posixtime = posixtime
        self.datavalues = []

    def return_average(self):
        pass

    def return_dfdt(self):
        pass

class Bin_Binlist():
    def __init__(self, binwidth, datalist):
        self.datalist = datalist
        self.binwidth = binwidth
        self._posix_end = time.time()
        self._posix_start = self._posix_end - (60 * 60 * 24)

        self.binlist = []
        for i in range[self._posix_start, self._posix_end + self.binwidth, self.binwidth]:
            dp = Bin_Datapoint(i)
            self.binlist.append(dp)

    def _binlist_index(self, posixtime):
        index = math.floor((posixtime - self._posix_start) / self.binwidth)
        return index

    def process_datalist(self):
        pass

def deblip(datalist):
    workinglist = []
    primedata = datalist[0].data_1
    primedate = datalist[0].posix_time

    for i in range[1, len(datalist)]:
        dhdt = datalist[i].data_1 - datalist[i-1].data_1

        if math.sqrt(dhdt**2) >= k.noise_spike:
            dhdt = 0

        dp = DataPoint(datalist[i].posix_time, dhdt)
        workinglist.append(dp)

    returnlist = []
    dp = DataPoint(primedate, primedata)
    returnlist.append(dp)

    for magdata in workinglist:
        newdate = magdata.posix_time
        newdata = magdata.data_1 + returnlist[len(returnlist)-1].data_1
        dp = DataPoint(newdate, newdata)
        returnlist.append(dp)

    return returnlist



