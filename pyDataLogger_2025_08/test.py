import mgr_database
import mgr_matplot
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
            try:
                result = round(np.mean(self.dp_data), 4)
            except:
                print("Corrupt data in array")
                print(self.dp_data)
        return result


def get_index(psx_start, psx_current, step):
    index = int((psx_current - psx_start) / step)
    return index

# -------------------- For 1 day readings --------------------------
time_end = int(time.time())
time_start = time_end - (60 * 60 * 24)
# This will allow us to convert readings pert second to readigs per minute, hour, etc.
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

utc_datelist = []
pressure_data = []
for item in datapointlist:
    data = item.get_avg_data()
    utcdate = standard_stuff.posix2utc(item.posixstamp, '%Y-%m-%d %H:%M')
    utc_datelist.append(utcdate)
    pressure_data.append(data)

print("Plot pressure one day")
savefile = k.dir_images + os.sep + "1days_pressure.png"
mgr_matplot.plot_time_data(utc_datelist, pressure_data, 60,"Pressure One Day", savefile)

print("Plot detrended pressure one day")
savefile = k.dir_images + os.sep + "1days_dt_pressure.png"
readings_per_tick = 60
halfwindow = 60 * 1.5
mgr_matplot.plot_detrended(utc_datelist, pressure_data, readings_per_tick, halfwindow, "Detrended Pressure One Day", savefile)

# -------------------- For 7 day readings --------------------------
time_end = int(time.time())
time_start = time_end - (60 * 60 * 24 * 7)
# This will allow us to convert readings pert second to readigs per minute, hour, etc.
time_step = 60
queryresult = mgr_database.db_get_pressure(time_start)

# Parse out a CSV list to check in spreadsheet
csvdata = []
for item in queryresult:
    dp = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S') + "," + str(item[1])
    csvdata.append(dp)
with open("current_csvdata.csv", "w") as c:
    for item in csvdata:
        line = str(item) + "\r\n"
        c.write(line)
c.close()

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

# Create two lists, time and data to be passed into the graphing methods
utc_datelist = []
pressure_data = []
for item in datapointlist:
    data = item.get_avg_data()
    utcdate = standard_stuff.posix2utc(item.posixstamp, '%Y-%m-%d %H:%M')
    utc_datelist.append(utcdate)
    pressure_data.append(data)

print("Plot pressure seven days")
savefile = k.dir_images + os.sep + "7days_pressure.png"
readings_per_tick = 60 * 6
mgr_matplot.plot_time_data(utc_datelist, pressure_data, readings_per_tick,"Pressure Seven Days", savefile)

print("Plot detrended pressure seven days")
savefile = k.dir_images + os.sep + "7days_dt_pressure.png"
halfwindow = 60 * 1.5
mgr_matplot.plot_detrended(utc_datelist, pressure_data, readings_per_tick, halfwindow, "Detrended Pressure Seven Days", savefile)

