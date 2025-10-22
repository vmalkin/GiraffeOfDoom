import mgr_database
import mgr_matplot
import time
import os
from datetime import datetime, timezone
import constants as k
import standard_stuff
import class_aggregator
import fft_discrete_steps

time_end = time.time()
time_start_7d = time_end - (60 * 60 * 24 * 7)

result_7d = mgr_database.db_data_get(time_start_7d)
start_7d = standard_stuff.posix2utc(result_7d[0][0], '%Y-%m-%d %H:%M')
print(f"7 Day start time is {start_7d}")

result_1d = result_7d[-86400 * int(1 / k.sensor_reading_frequency):]
start_1d = standard_stuff.posix2utc(result_1d[0][0], '%Y-%m-%d %H:%M')
print(f"1 Day start time is {start_1d}")
#
# result_6hr = result_7d[-21600 * readings_per_second:]
# start_6hr = standard_stuff.posix2utc(result_6hr[0][0], '%Y-%m-%d %H:%M')
# print(f"6hr start time is {start_6hr}")
# ========================================================================================
# We want the following plots.
# Spectrum of last 24 hours. Full resolution Data.
# Hourly plots for the past 24 hours. Data aggregated into 1-minute bins
# Plot of the past 7 days. Data aggregated up to 60-minute bins depending on smoothness of plot.
# DATETIMES shuld be passed into matplotlib as a datetime object.
# ========================================================================================
try:
    print("Barometric Spectrogram - Past 24 hours")
    window = 10
    aggregate_array = class_aggregator.aggregate_data(window, result_7d)
    aggregate_array.pop(0)

    plot_utc = []
    plot_press = []
    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
        plot_utc.append(tim)
        plot_press.append(prs)

    df = "%d %H:%M"
    title = "Spectrogram of Barometric Pressure"
    savefile = k.dir_images + os.sep + "spectrum_press.png"
    mgr_matplot.plot_spectrum(df, plot_press, plot_utc, 1, 0, 25, title, savefile)
except:
    pass

# =============================================================================================================
print("Tiltmeter - 24, hourly plots")
aggregate_array = result_1d
aggregate_array.pop(0)
plot_utc = []
plot_seismo = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i][0]
    tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
    siz = aggregate_array[i][1]
    plot_utc.append(tim)
    plot_seismo.append(siz)

# Convert distance readings to rate of change.
# This is similar to traditional seismograph display
dxdt = []
for i in range(1, len(plot_seismo)):
    # dx = plot_seismo[i]
    dx = plot_seismo[i] - plot_seismo[i - 1]
    dxdt.append(dx)
plot_utc.pop(0)

avgwindow = 10 * 5
smoothe_seismo = standard_stuff.filter_average(dxdt, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]

ticks = 20
df = "%d  %H:%M"
title = "Tiltmeter One Day dx/dt"
savefolder = k.dir_images
mgr_matplot.plot_hourlyplots(df, plot_utc, smoothe_seismo, title, savefolder)

# =============================================================================================================
print("Tiltmeter - 1 Day")
aggregate_array = result_1d
aggregate_array.pop(0)
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
wrapper = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i][0]
    tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
    siz = aggregate_array[i][1]
    tmp = aggregate_array[i][2]
    prs = aggregate_array[i][3]
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)

spectrum_utc = plot_utc
spectrum_seismo = plot_seismo

avgwindow = 20
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]
wrapper.append(smoothe_seismo)
wrapper.append(plot_press)
wrapper.append(plot_temp)

ticks = 20
df = "%d  %H:%M"
title = "Tiltmeter One Day"
savefile = k.dir_images + os.sep + "one_day.png"
mgr_matplot.plot_multi(df, plot_utc, wrapper, ticks, title, savefile)

df = "%d %H:%M"
title = "Spectrogram of Tilt Readings"
savefile = k.dir_images + os.sep + "spectrum_seismo.png"
mgr_matplot.plot_spectrum(df, spectrum_seismo, spectrum_utc, 1, -10, 20, title, savefile)


# =============================================================================================================
# A special instance here where we will decimate the volume of data
print("Tiltmeter - 7 Days")
# decimate data for this.
window = 10
aggregate_array = class_aggregator.aggregate_data(window, result_7d)
aggregate_array.pop(0)

wrapper = []
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []

for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i].get_avg_posix()
    tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
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
wrapper.append(smoothe_seismo)
wrapper.append(plot_press)
wrapper.append(plot_temp)

ticks = 240
df = "%d  %H:%M"
title = "Tiltmeter One Week"
savefile = k.dir_images + os.sep + "seven_day.png"
mgr_matplot.plot_multi(df, plot_utc, wrapper, ticks, title, savefile)

# =============================================================================================================
print("FFT - 7 Days")
# Convert distance readings to rate of change.
# This is similar to traditional seismograph display
# aggregate_array = result_7d
# aggregate_array.pop(0)
# plot_utc = []
# plot_seismo = []
#
# for i in range(1, len(aggregate_array)):
#     tim = aggregate_array[i][0]
#     tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
#     siz = aggregate_array[i][1]
#     plot_utc.append(tim)
#     plot_seismo.append(siz)
#
# dxdt = []
# for i in range(1, len(plot_seismo)):
#     # dx = plot_seismo[i]
#     dx = plot_seismo[i] - plot_seismo[i - 1]
#     d = ['x', dx]
#     dxdt.append(d)
# plot_utc.pop(0)

fft_discrete_steps.wrapper(result_7d)
timefinish = time.time()
print(f"Elapsed seconds to process: {timefinish - time_end}")
