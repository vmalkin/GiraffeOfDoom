import mgr_database
import mgr_matplot
import time
import os
import constants as k
import standard_stuff
import class_aggregator

time_end = time.time()
time_start_1d = time_end - (60 * 60 * 24)
time_start_7d = time_end - (60 * 60 * 24 * 7)

result_1d = mgr_database.db_get_pressure(time_start_1d)
result_7d = mgr_database.db_get_pressure(time_start_7d)

# ========================================================================================
# We want the following plots.
# Spectrum of last 24 hours. Full resolution Data.
# Hourly plots for the past 24 hours. Data aggregated into 1-minute bins
# Plot of the past 7 days. Data aggregated up to 60-minute bins depending on smoothness of plot.
# ========================================================================================
print("Tiltmeter Spectrogram - Past 24 hours")
utc_datelist = []
seismo_data = []
window = 2  # 0.2 second
plotdata = class_aggregator.aggregate_data(window, result_1d)
for item in plotdata:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist.append(utc)
    seismo_data.append(seismo)
savefile = k.dir_images + os.sep + "spectrum.png"
mgr_matplot.plot_spectrum(seismo_data, utc_datelist, window, savefile)

print("Tiltmeter - Past 24 hours")
utc_datelist = []
seismo_data = []
window = 60  # one minute
plotdata = class_aggregator.aggregate_data(window, result_1d)
for item in plotdata:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M')
    # utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist.append(utc)
    seismo_data.append(seismo)
savefile = k.dir_images + os.sep + "one_day.png"
mgr_matplot.plot_time_data(utc_datelist, seismo_data, 100,"Tiltmeter One Day", savefile)

print("Tiltmeter - Hourly plot")
utc_datelist = []
seismo_data = []
window = 2  # one minute
plotdata = class_aggregator.aggregate_data(window, result_1d)
for item in plotdata:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    # utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist.append(utc)
    seismo_data.append(seismo)
savepath = k.dir_images
mgr_matplot.plot_hourly_array(utc_datelist, seismo_data, savepath)

print("Tiltmeter - 7 Days")
utc_datelist = []
seismo_data = []
window = 60 * 60 # one hour
plotdata = class_aggregator.aggregate_data(window, result_7d)
for item in plotdata:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M')
    seismo = item[1]
    utc_datelist.append(utc)
    seismo_data.append(seismo)
savefile = k.dir_images + os.sep + "seven_day.png"
mgr_matplot.plot_time_data(utc_datelist, seismo_data, 100,"Tiltmeter One Week", savefile)