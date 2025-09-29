import mgr_database
import mgr_matplot
import time
import os
import constants as k
import standard_stuff
import numpy as np


time_end = time.time()
time_start_24h = time_end - (60 * 60 * 24)
time_start_7d = time_end - (60 * 60 * 24 * 7)
# This will allow us to convert readings pert second to readigs per minute, hour, etc.
# data_steps = 60
result_24h = mgr_database.db_get_pressure(time_start_24h)
result_7d = mgr_database.db_get_pressure(time_start_7d)

utc_datelist_24hr = []
seismo_data_24hr = []
for item in result_24h:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist_24hr.append(utc)
    seismo_data_24hr.append(seismo)

utc_datelist_7d = []
seismo_data_7d = []
for item in result_7d:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist_7d.append(utc)
    seismo_data_7d.append(seismo)

filter_window = 5 * 60
filtered_seismo_data = standard_stuff.filter_median(seismo_data_24hr, filter_window)
filtered_utc_datelist = utc_datelist_24hr[filter_window: -1 * filter_window]

print("Tiltmeter - Past 24 hours")
savefile = k.dir_images + os.sep + "1days_tilt.png"
mgr_matplot.plot_time_data(filtered_utc_datelist, filtered_seismo_data, 30000,"Tiltmeter One Day", savefile)

print("Tiltmeter Spectrogram - Past 24 hours")
savefile = k.dir_images + os.sep + "spectrum.png"
mgr_matplot.plot_spectrum(seismo_data_24hr, utc_datelist_24hr, savefile)

print("Tiltmeter - 7 day")
filter_window = 5 * 60 * 60
filtered_seismo_data_7d = standard_stuff.filter_median(seismo_data_7d, filter_window)
filtered_utc_datelist_7d = utc_datelist_7d[filter_window: -1 * filter_window]
plot_data = []
plot_utc = []
step_interval = 5 * 60 * 60
for i in range(0, len(filtered_seismo_data_7d)):
    if i % step_interval == 0:
        plot_data.append(filtered_seismo_data_7d[i])
        plot_utc.append(filtered_utc_datelist_7d[i])
savefile = k.dir_images + os.sep + "7d_tilt.png"
mgr_matplot.plot_time_data(plot_utc, plot_data, 30000,"Tiltmeter Seven Day", savefile)

print("Tiltmeter - hourly")
mgr_matplot.plot_hourly_array(filtered_utc_datelist, filtered_seismo_data, k.dir_images)

