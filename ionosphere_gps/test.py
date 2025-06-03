import copy
import standard_stuff
import mgr_database
import mgr_matplot
import time
import os
import constants as k
import numpy as np

nan_value = np.nan

timenow = int(time.time())
timestart = timenow - (60 * 60 * 24)
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
    psx = i
    utc = standard_stuff.posix2utc(psx, '%m-%d %H:%M:%S')
    timebins.append(str(utc))
    # blankdata.append(nan_value)
    blankdata.append(0)

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

    if snr == '':
        snr = nan_value

    blankdataindex = psx_time - t_start
    datablob[sat_id][blankdataindex] = snr

diffsblob = []
datablob.pop(0)
for dataseries in datablob:
    diffsseries = []
    for i in range(1, len(dataseries)):
        j = dataseries[i] - dataseries[i - 1]
        diffsseries.append(j)
    # diffsseries = standard_stuff.filter_median(diffsseries, 1)
    diffsblob.append(diffsseries)

savefile = k.dir_images + os.sep + "simple_snr.png"
mgr_matplot.plot_time_snr(diffsblob, timebins, savefile)

