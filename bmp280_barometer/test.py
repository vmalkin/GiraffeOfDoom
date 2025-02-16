import mgr_database
import mgr_matplot
# import mgr_emd
import time
import os
import constants as k
import standard_stuff
import numpy as np


class DataPoint:
    def __init__(self, posixstamp, step):
        self.posixstamp = posixstamp
        self.step = step
        self.dp_data = []

    def get_avg_data(self):
        result = None
        if len(self.dp_data) > 0:
            result = round(np.mean(self.dp_data), 4)
        return result


def get_index(psx_start, psx_current, step):
    index = int((psx_start - psx_current) / step)
    return index

time_end = int(time.time())
time_start = time_end - (60 * 60 * 24)

# This will allow us to convert readings pert second toreadigs per minute, hour, etc.
time_step = 60
queryresult = mgr_database.db_get_pressure(time_start)

# Set up array of datapoints
datapointlist = []
for i in range(time_start, time_end + 60, time_step):
    d = DataPoint(i, time_step)
    datapointlist.append(d)

for item in queryresult:
    posixtime = item[0]
    pressure = item[1]
    index = get_index(time_start, posixtime, time_step)
    datapointlist[index].dp_data.append(pressure)

# Create two lists, time and data to be passed nto the graphing methods
utc_datelist = []
pressure_data = []
for item in datapointlist:
    data = item.get_avg_data()
    utcdate = standard_stuff.posix2utc(item.posixstamp, '%Y-%m-%d %H:%M:%S')
    utc_datelist.append(utcdate)
    pressure_data.append(data)

# print("Plot pressure seven days")
#
# savefile = k.dir_images + os.sep + "7days_pressure.png"
# readings_per_minute = 1
# decimation = int(60 / readings_per_minute)
# readings_per_tick = readings_per_minute * 60 * 12
# mgr_matplot.plot_time_data(queryresult, decimation, readings_per_tick, "Pressure Seven Days",savefile)

# print("Plot detrended pressure seven days")
# savefile = k.dir_images + os.sep + "7days_dt_pressure.png"
# readings_per_minute = 2
# decimation = int(60 / readings_per_minute)
# readings_per_tick = readings_per_minute * 60 * 12
# halfwindow = int(60 / decimation) * 60 * 1.5
# print("*** Detrended half window size: ", halfwindow)
# mgr_matplot.plot_detrended(queryresult, decimation, readings_per_tick, halfwindow, "Detrended Pressure Seven Day", savefile)
#
print("Plot pressure one day")
mgr_matplot.plot_time_data(utc_datelist, pressure_data,"Pressure One Day", savefile)

#
# print("Plot standard deviation one day")
# readings_per_minute = 30
# decimation = int(60 / readings_per_minute)
# readings_per_tick = readings_per_minute * 60 * 1
# halfwindow = int(60 / decimation) * 5
# savefile = k.dir_images + os.sep + "stats.png"
# mgr_matplot.plot_stats(queryresult, decimation, readings_per_tick, halfwindow, savefile)
#
# print("Plot detrended pressure one day")
# savefile = k.dir_images + os.sep + "1days_dt_pressure.png"
# readings_per_minute = 1
# decimation = int(60 / readings_per_minute)
# readings_per_tick = readings_per_minute * 60 * 1
# halfwindow = int(60 / decimation) * 5
# print("*** Detrended half window size: ", halfwindow)
# mgr_matplot.plot_detrended(queryresult, decimation, readings_per_tick, halfwindow, "Detrended Pressure One Day", savefile)
