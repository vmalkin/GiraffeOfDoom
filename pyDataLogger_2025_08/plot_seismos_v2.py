import mgr_database
import mgr_matplot
import time
import os
import datetime
import constants as k
import standard_stuff
import class_aggregator

time_end = time.time()
time_start_7d = time_end - (60 * 60 * 24 * 7)
result_7d = mgr_database.db_data_get(time_start_7d)
result_1d = result_7d[-86400:]
result_6hr = result_7d[-21600:]

# ========================================================================================
# We want the following plots.
# Spectrum of last 24 hours. Full resolution Data.
# Hourly plots for the past 24 hours. Data aggregated into 1-minute bins
# Plot of the past 7 days. Data aggregated up to 60-minute bins depending on smoothness of plot.
# DATETIMES shuld be passed into matplotlib as a datetime object.
# ========================================================================================
print("Tiltmeter - 6hr")
aggregate_array = result_6hr
aggregate_array.pop(0)
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i][0]
    tim = datetime.datetime.fromtimestamp(tim)  # datetime object
    siz = aggregate_array[i][1]
    plot_utc.append(tim)
    plot_seismo.append(siz)

avgwindow = 40
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
ticks = 30
ymin = 451.5
ymax = 453
df = "%d %H:%M"
title = "Tiltmeter 6 Hours"
savefile = k.dir_images + os.sep + "six_hour.png"
mgr_matplot.plot_time_data(df, plot_utc, smoothe_seismo, ticks, ymin, ymax, title, savefile)

print("Barometric Spectrogram - Past 24 hours")
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(result_1d)):
    tt = result_1d[i][0]
    tim = datetime.datetime.fromtimestamp(tt)  # datetime object
    prs = result_1d[i][3]
    plot_utc.append(tim)
    plot_press.append(prs)
df = "%d %H:%M"
title = "Spectrogram of Barometric Pressure"
savefile = k.dir_images + os.sep + "spectrum_press.png"
mgr_matplot.plot_spectrum(df, plot_press, plot_utc, 1, 0, 30, title, savefile)

print("Tiltmeter - 1 Day")
aggregate_array = result_1d
aggregate_array.pop(0)
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i][0]
    tim = datetime.datetime.fromtimestamp(tim)  # datetime object
    siz = aggregate_array[i][1]
    tmp = aggregate_array[i][2]
    prs = aggregate_array[i][3]
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)

avgwindow = 40
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]

ticks = 120
ymin = 451.5
ymax = 453
df = "%d  %H:%M"
title = "Tiltmeter One Day"
savefile = k.dir_images + os.sep + "one_day.png"
mgr_matplot.plot_time_data(df, plot_utc, smoothe_seismo,  ticks,ymin, ymax, title, savefile)
ymin = None
ymax = None
df = "%d  %H:%M"
title = "Pressure One Day"
savefile = k.dir_images + os.sep + "one_press.png"
mgr_matplot.plot_time_data(df, plot_utc, plot_press,  ticks,ymin, ymax, title, savefile)
ymin = None
ymax = None
df = "%d  %H:%M"
title = "Temperature One Day"
savefile = k.dir_images + os.sep + "one_temp.png"
mgr_matplot.plot_time_data(df, plot_utc, plot_temp,  ticks,ymin, ymax, title, savefile)

# A special instance here where we will decimate the volume of data
print("Tiltmeter - 7 Days")
# decimate data for this.
window = 10
aggregate_array = class_aggregator.aggregate_data(window, result_7d)
aggregate_array.pop(0)
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i].get_avg_posix()
    tim = datetime.datetime.fromtimestamp(tim)  # datetime object
    siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
    tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
    prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)

# Scatterplots are here to use the 7 day data that's already been processed. No need to duplicate things.
print("Tiltmeter - Scatterplots")
sct_seis = standard_stuff.filter_median(plot_seismo, 2)
sct_press = standard_stuff.filter_median(plot_press, 2)
sct_temp = standard_stuff.filter_median(plot_temp, 2)
savefile = k.dir_images + os.sep + "sctr_tilt_temp.png"
mgr_matplot.plot_scatterplot(sct_temp, sct_seis, "7 Day Tilt vs Temperature", savefile)
savefile = k.dir_images + os.sep + "sctr_tilt_press.png"
mgr_matplot.plot_scatterplot(sct_press, sct_seis, "7 Day Tilt vs Air Pressure", savefile)

avgwindow = 40
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]

ticks = 240
ymin = 451.5
ymax = 453
df = "%d  %H:%M"
title = "Tiltmeter One Week"
savefile = k.dir_images + os.sep + "seven_day.png"
mgr_matplot.plot_time_data(df, plot_utc, smoothe_seismo,  ticks,ymin, ymax, title, savefile)
ymin = None
ymax = None
df = "%d  %H:%M"
title = "Pressure One Week"
savefile = k.dir_images + os.sep + "seven_press.png"
mgr_matplot.plot_time_data(df, plot_utc, plot_press,  ticks,ymin, ymax, title, savefile)
ymin = None
ymax = None
df = "%d  %H:%M"
title = "Temperature One Week"
savefile = k.dir_images + os.sep + "seven_temp.png"
mgr_matplot.plot_time_data(df, plot_utc, plot_temp,  ticks,ymin, ymax, title, savefile)


print("Tiltmeter - One Day dx/dt")
aggregate_array = result_1d
aggregate_array.pop(0)
plot_utc = []
plot_seismo = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i][0]
    tim = datetime.datetime.fromtimestamp(tim)  # datetime object
    siz = aggregate_array[i][1]
    plot_utc.append(tim)
    plot_seismo.append(siz)

# Convert distance readings to rate of change.
# This is similar to traditional seismograph display
dxdt = []
for i in range(1, len(plot_seismo)):
    dx = plot_seismo[i] - plot_seismo[i - 1]
    dxdt.append(dx)
plot_utc.pop(0)

df = "%d  %H:%M"
title = "7 Day Spectrogram of Tilt Readings"
savefile = k.dir_images + os.sep + "spectrum_seven.png"
mgr_matplot.plot_spectrum(df, plot_seismo, plot_utc, 1, -140, -15, title, savefile)

avgwindow = 120
smoothe_seismo = standard_stuff.filter_average(dxdt, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]

ticks = 60
ymin = -0.005
ymax = 0.005
df = "%d  %H:%M"
title = "Tiltmeter - One Day dx/dt"
savefile = k.dir_images + os.sep + "dxdt.png"
mgr_matplot.plot_time_data(df, plot_utc, smoothe_seismo, ticks, ymin, ymax, title, savefile)

timefinish = time.time()
print(f"Elapsed seconds to process: {timefinish - time_end}")