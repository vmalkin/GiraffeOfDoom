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
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(result_1d)):
    tt = result_1d[i][0]
    # tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tt, '%d  %H:%M')
    siz = result_1d[i][1]
    # tmp = result_1d[i][2]
    # prs = result_1d[i][3]
    plot_utc.append(tim)
    plot_seismo.append(siz)
    # plot_temp.append(tmp)
    # plot_press.append(prs)
savefile = k.dir_images + os.sep + "spectrum.png"
mgr_matplot.plot_spectrum(plot_seismo, plot_utc, 1, savefile)
# savefile = k.dir_images + os.sep + "spectrum_press.png"
# mgr_matplot.plot_spectrum(plot_press, plot_utc, 1, savefile)

print("Tiltmeter - Past 6 hours")
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(result_6hr)):
    tt = result_6hr[i][0]
    # tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tt, '%d  %H:%M:%S')
    siz = result_6hr[i][1]
    tmp = result_6hr[i][2]
    prs = result_6hr[i][3]
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)
avgwindow = 15
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
smoothe_temp = standard_stuff.filter_average(plot_temp, avgwindow)
smoothe_press = standard_stuff.filter_average(plot_press, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
smoothe_temp = standard_stuff.filter_average(smoothe_temp, avgwindow)
smoothe_press = standard_stuff.filter_average(smoothe_press, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]

ticks = 1200
ymin = 451.5
ymax = 453
savefile = k.dir_images + os.sep + "six_hour.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_seismo, ticks, ymin, ymax, "Tiltmeter Six Hours", savefile)
ymin = None
ymax = None
savefile = k.dir_images + os.sep + "six_pressure.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_press, ticks, ymin, ymax,"Pressure Six Hours", savefile)
ymin = None
ymax = None
savefile = k.dir_images + os.sep + "six_temp.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_temp, ticks, ymin, ymax,"Temperature Six Hours", savefile)

print("Tiltmeter - Past 24 hours")
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(result_1d)):
    tt = result_1d[i][0]
    # tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tt, '%d  %H:%M')
    siz = result_1d[i][1]
    tmp = result_1d[i][2]
    prs = result_1d[i][3]
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)
avgwindow = 60
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
smoothe_temp = standard_stuff.filter_average(plot_temp, avgwindow)
smoothe_press = standard_stuff.filter_average(plot_press, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
smoothe_temp = standard_stuff.filter_average(smoothe_temp, avgwindow)
smoothe_press = standard_stuff.filter_average(smoothe_press, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]

ymin = 451.5
ymax = 453
savefile = k.dir_images + os.sep + "one_day.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_seismo, 120,ymin, ymax,"Tiltmeter One Day", savefile)
ymin = None
ymax = None
savefile = k.dir_images + os.sep + "one_press.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_press,  120,ymin, ymax,"Pressure One Day", savefile)
ymin = None
ymax = None
savefile = k.dir_images + os.sep + "one_temp.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_temp,  120,ymin, ymax,"Temperature One Day", savefile)

print("Tiltmeter - 7 Days")
plot_utc = []
plot_seismo = []
plot_temp = []
plot_press = []
for i in range(1, len(result_7d)):
    tt = result_7d[i][0]
    # tim = aggregate_array[i].get_avg_posix()
    tim = standard_stuff.posix2utc(tt, '%d  %H:%M')
    siz = result_7d[i][1]
    tmp = result_7d[i][2]
    prs = result_7d[i][3]
    plot_utc.append(tim)
    plot_seismo.append(siz)
    plot_temp.append(tmp)
    plot_press.append(prs)
avgwindow = 60
smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
smoothe_temp = standard_stuff.filter_average(plot_temp, avgwindow)
smoothe_press = standard_stuff.filter_average(plot_press, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]
smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
smoothe_temp = standard_stuff.filter_average(smoothe_temp, avgwindow)
smoothe_press = standard_stuff.filter_average(smoothe_press, avgwindow)
plot_utc = plot_utc[avgwindow:-avgwindow]

ticks = 120
ymin = 451.5
ymax = 453
savefile = k.dir_images + os.sep + "seven_day.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_seismo,  ticks,ymin, ymax,"Tiltmeter One Week", savefile)
ymin = None
ymax = None
savefile = k.dir_images + os.sep + "seven_press.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_press,  ticks,ymin, ymax,"Pressure One Week", savefile)
ymin = None
ymax = None
savefile = k.dir_images + os.sep + "seven_temp.png"
mgr_matplot.plot_time_data(plot_utc, smoothe_temp,  ticks,ymin, ymax,"Temperature One Week", savefile)