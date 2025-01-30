import mgr_database
import mgr_matplot
import time
import os
import constants as k

print("Plot pressure seven days")
now = int(time.time())
timeinterval = now - (60 * 60 * 24 * 7)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "7days_pressure.png"
readings_per_minute = 1
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 12
mgr_matplot.plot_time_data(queryresult, decimation, readings_per_tick, "Seven Days",savefile)

print("Plot pressure one day")
timeinterval = now - (60 * 60 * 24)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "pressure_24.png"
readings_per_minute = 1
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 1
mgr_matplot.plot_time_data(queryresult, decimation, readings_per_tick,"One Day", savefile)

print("Plot standard deviation one day")
readings_per_minute = 30
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 1
halfwindow = int(60 / decimation) * 5
savefile = k.dir_images + os.sep + "stats.png"
mgr_matplot.plot_stats(queryresult, decimation, readings_per_tick, halfwindow, savefile)

print("Plot detrended pressure one day")
savefile = k.dir_images + os.sep + "detrended_24.png"
readings_per_minute = 1
decimation = int(60 / readings_per_minute)
readings_per_tick = readings_per_minute * 60 * 1
halfwindow = int(60 / decimation) * 5
mgr_matplot.plot_detrended(queryresult, decimation, readings_per_tick, halfwindow, savefile)

