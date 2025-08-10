import mgr_database
import mgr_matplot
import time
import os
import constants as k
import standard_stuff
import numpy as np


class DataPoint:
    def __init__(self, posixstamp):
        self.posixstamp = posixstamp
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
time_end = time.time()
time_start = time_end - (60 * 60 * 24)
# This will allow us to convert readings pert second to readigs per minute, hour, etc.
data_steps = 60
queryresult = mgr_database.db_get_pressure(time_start)

# Set up array of datapoints
# datapointlist = []
# for i in range(int(time_start), int(time_end) + data_steps, data_steps):
#     d = DataPoint(i)
#     datapointlist.append(d)
#
# for item in queryresult:
#     posixtime = int(item[0])
#     seismodata = item[1]
#     index = get_index(time_start, posixtime, time_step)
#     datapointlist[index].dp_data.append(seismodata)

utc_datelist = []
seismo_data = []
for item in queryresult:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist.append(utc)
    seismo_data.append(seismo)

# for item in datapointlist:
#     data = item.get_avg_data()
#     utcdate = standard_stuff.posix2utc(item.posixstamp, '%Y-%m-%d %H:%M:%S.%f')
#     utc_datelist.append(utcdate)
#     pressure_data.append(data)

filter_window = 5 * 30
filtered_seismo_data = standard_stuff.filter_average(seismo_data, filter_window)
filtered_utc_datelist = utc_datelist[filter_window: -1 * filter_window]

print("Tiltmeter - hourly")
mgr_matplot.plot_hourly_array(utc_datelist, seismo_data, k.dir_images)

print("Tiltmeter - Past 24 hours")
savefile = k.dir_images + os.sep + "1days_tilt.png"
mgr_matplot.plot_time_data(filtered_utc_datelist, filtered_seismo_data, 30000,"Tiltmeter One Day", savefile)

print("Tiltmeter Spectrogram - Past 24 hours")
savefile = k.dir_images + os.sep + "spectrum.png"
mgr_matplot.plot_spectrum(seismo_data, savefile)


# csvdata = []
# for item in queryresult:
#     # dp = str(item[0]) + "," + str(item[1])
#     dp = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f') + "," + str(item[1])
#     csvdata.append(dp)
# with open("current_csvdata.csv", "w") as c:
#     for item in csvdata:
#         line = str(item) + "\r\n"
#         c.write(line)
# c.close()
