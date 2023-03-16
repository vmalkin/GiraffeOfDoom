import time
import datetime
import math
import mgr_database
import numpy as np
from calendar import timegm
from statistics import mean, median

nullvalue = None


class Dday:
    def __init__(self, datestring):
        self.hours = []
        self.label = datestring
        for i in range(0, 24):
            h = Dhours(i)
            self.hours.append(h)

class Dhours:
    def __init__(self, label):
        self.label = label
        self.minutes = []
        for i in range(0, 60):
            m = Dmins(i)
            self.minutes.append(m)


class Dmins:
    def __init__(self, label):
        self.label = label
        self.datavalue = []

    def get_average(self):
        returnresult = nullvalue
        if len(self.datavalue) > 0:
            returnresult = mean(self.datavalue)
        return returnresult

def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


utctime = "2023-02-20 00:00"
starttime = utc2posix(utctime, '%Y-%m-%d %H:%M')
day = 60 * 60 * 24 * 14
actualstart = starttime - day

alt = 40
# The result of the query gets passed into all plotting functions
result = mgr_database.qry_get_last_24hrs(actualstart, alt)
result = np.array(result)

start = int(result[0][1])
end = int(result[len(result) - 1][1])
day = 60 * 60 * 24
# duration = (end - start) / day
# duration = math.ceil(duration)

days = []
for i in range(start, end, day):
    dd = Dday(i)
    days.append(dd)

for row in result:
    psx = int(row[1])
    data = float(row[5])
    hr = int(posix2utc(psx, '%H'))
    mn = int(posix2utc(psx, '%M'))
    idx = int(math.floor((psx - start) / day))
    days[idx].hours[hr].minutes[mn].datavalue.append(data)
    # print(days[idx].hours[hr].minutes[mn].get_average())



# mgr_plot.wrapper(result, k.comport)




