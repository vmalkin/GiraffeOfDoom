import mgr_database
import mgr_matplot
# import mgr_emd
import time
import os
import constants as k
import standard_stuff

print("Plot pressure seven days")
now = int(time.time())
timeinterval = now - (60 * 60 * 24 * 7)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "7days_pressure.png"
readings_per_minute = 1
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 12
mgr_matplot.plot_time_data(queryresult, decimation, readings_per_tick, "Pressure Seven Days",savefile)

print("Plot detrended pressure seven days")
savefile = k.dir_images + os.sep + "7days_dt_pressure.png"
readings_per_minute = 2
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 12
halfwindow = int(60 / decimation) * 60 * 1.5
print("*** Detrended half window size: ", halfwindow)
mgr_matplot.plot_detrended(queryresult, decimation, readings_per_tick, halfwindow, "Detrended Pressure Seven Day", savefile)

# print("Plot standard deviation seven day")
# savefile = k.dir_images + os.sep + "7days_stats.png"
# mgr_matplot.plot_stats(queryresult, decimation, readings_per_tick, halfwindow, savefile)

print("Plot pressure one day")
timeinterval = now - (60 * 60 * 24)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "1days_pressure.png"
readings_per_minute = 1
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 1
mgr_matplot.plot_time_data(queryresult, decimation, readings_per_tick,"Pressure One Day", savefile)

print("Plot standard deviation one day")
readings_per_minute = 30
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 1
halfwindow = int(60 / decimation) * 5
savefile = k.dir_images + os.sep + "stats.png"
mgr_matplot.plot_stats(queryresult, decimation, readings_per_tick, halfwindow, savefile)

print("Plot detrended pressure one day")
savefile = k.dir_images + os.sep + "1days_dt_pressure.png"
readings_per_minute = 1
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 1
halfwindow = int(60 / decimation) * 5
print("*** Detrended half window size: ", halfwindow)
mgr_matplot.plot_detrended(queryresult, decimation, readings_per_tick, halfwindow, "Detrended Pressure One Day", savefile)

# savefile = k.dir_images + os.sep + "emd.png"
# mgr_emd.wrapper(queryresult, savefile)
