import mgr_database
import mgr_matplot
import time
import os
import constants as k
import standard_stuff
import class_aggregator

time_end = time.time()
time_start_6hr = time_end - (60 * 60 * 7)
time_start_1d = time_end - (60 * 60 * 25)
time_start_7d = time_end - (60 * 60 * 24 * 7)

result_6hr = mgr_database.db_data_get(time_start_6hr)
result_1d = mgr_database.db_data_get(time_start_1d)
result_7d = mgr_database.db_data_get(time_start_7d)

# ========================================================================================
# We want the following plots.
# Spectrum of last 24 hours. Full resolution Data.
# Hourly plots for the past 24 hours. Data aggregated into 1-minute bins
# Plot of the past 7 days. Data aggregated up to 60-minute bins depending on smoothness of plot.
# ========================================================================================
print("Tiltmeter Spectrogram - Past 24 hours")
utc_datelist = []
seismo_data = []
window = 1  # 0.2 second
aggregate_array = class_aggregator.aggregate_data(window, result_1d)
aggregate_array.pop(0)

plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tim, '%d  %H:%M')
    siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
    tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
    prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)
savefile = k.dir_images + os.sep + "spectrum.png"
mgr_matplot.plot_spectrum(plot_seismo, plot_utc, window, savefile)
savefile = k.dir_images + os.sep + "spectrum_press.png"
mgr_matplot.plot_spectrum(plot_press, plot_utc, window, savefile)

print("Tiltmeter - Past 6 hours")
utc_datelist = []
seismo_data = []
window = 30  # one second
aggregate_array = class_aggregator.aggregate_data(window, result_6hr)
aggregate_array.pop(0)

plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tim, '%d  %H:%M')
    siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
    tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
    prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)
avgwindow = 5
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_seismo = plot_seismo[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]
plot_utc = plot_utc[avgwindow:-avgwindow]

savefile = k.dir_images + os.sep + "six_hour.png"
mgr_matplot.plot_time_data(plot_utc, plot_seismo, smoothe_seismo, 10,"Tiltmeter Six Hours", savefile)
savefile = k.dir_images + os.sep + "six_pressure.png"
mgr_matplot.plot_time_data(plot_utc, plot_press, None, 10,"Pressure Six Hours", savefile)
savefile = k.dir_images + os.sep + "six_temp.png"
mgr_matplot.plot_time_data(plot_utc, plot_temp, None, 10,"Temperature Six Hours", savefile)

print("Tiltmeter - Past 24 hours")
utc_datelist = []
seismo_data = []
window = 60  # one minute
aggregate_array = class_aggregator.aggregate_data(window, result_1d)
aggregate_array.pop(0)

plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tim, '%d  %H:%M')
    siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
    tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
    prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)

avgwindow = 5
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
plot_temp = plot_temp[avgwindow:-avgwindow]
plot_seismo = plot_seismo[avgwindow:-avgwindow]
plot_press = plot_press[avgwindow:-avgwindow]
plot_utc = plot_utc[avgwindow:-avgwindow]

savefile = k.dir_images + os.sep + "one_day.png"
mgr_matplot.plot_time_data(plot_utc, plot_seismo, smoothe_seismo, 120,"Tiltmeter One Day", savefile)
# mgr_matplot.plot_time_data(plot_utc, plot_seismo, None, 100,"Tiltmeter One Day", savefile)
savefile = k.dir_images + os.sep + "one_press.png"
mgr_matplot.plot_time_data(plot_utc, plot_press, None, 120,"Pressure One Day", savefile)
savefile = k.dir_images + os.sep + "one_temp.png"
mgr_matplot.plot_time_data(plot_utc, plot_temp, None, 120,"Temperature One Day", savefile)

print("Tiltmeter - 7 Days")
window = 60 * 5 # one hour
aggregate_array = class_aggregator.aggregate_data(window, result_7d)
aggregate_array.pop(0)

plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(aggregate_array)):
    tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tim, '%d  %H:%M')
    siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
    tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
    prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)
savefile = k.dir_images + os.sep + "seven_day.png"
mgr_matplot.plot_time_data(plot_utc, plot_seismo, None, 24,"Tiltmeter One Week", savefile)
savefile = k.dir_images + os.sep + "seven_press.png"
mgr_matplot.plot_time_data(plot_utc, plot_press, None, 24,"Pressure One Week", savefile)
savefile = k.dir_images + os.sep + "seven_temp.png"
mgr_matplot.plot_time_data(plot_utc, plot_temp, None, 24,"Temperature One Week", savefile)