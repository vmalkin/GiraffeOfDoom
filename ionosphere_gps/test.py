import copy

import mgr_database
import mgr_matplot
import time
import os
import constants as k
import numpy as np

nan_value = np.nan

timenow = int(time.time())
timestart = timenow - (60 * 60 * 24 * 1)
query_result = mgr_database.db_get_gsv(timestart, 15)

print("Plot polar")
timeinterval = timenow - (60 * 60 * 24)
savefile = k.dir_images + os.sep + "simple_polar.png"
mgr_matplot.plot_polar_noise(query_result, savefile)

# when dealing with gps data that might be at 10hz rate, multiply the posix values by
# 10 to deal with it.
t_start = int(timestart)
t_now = int(timenow)

timebins = []
blankdata = []
for i in range(t_start, t_now):
    timebins.append(t_start + i)
    blankdata.append(nan_value)

# set up the array to be passed in to graphing
datablob = []
for i in range(0, 40):
    # to make independent new copies of blank data array
    datablob.append(copy.deepcopy(blankdata))

for item in query_result:
    # ('GP', '01', 1748287326.1275165, 16, 221, 19)
    sat_id = int(item[1])
    psx_time = int(item[2])
    snr = item[5]
    alt = item[3]
    dp = [snr, alt]
    blankdataindex = psx_time - t_start
    datablob[sat_id][blankdataindex] = snr

datablob.pop(0)
for item in datablob:
    print(item[:30])

print(len(timebins))
print(len(datablob[1]))
savefile = k.dir_images + os.sep + "simple_snr.png"
mgr_matplot.plot_time_snr(datablob, timebins, savefile)

