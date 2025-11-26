import mgr_database
import time
import constants as k
import plotter_phaseportrait
import plotter_spectrograms
import plotter_combo1day
import plotter_combo7day

print(f'Querying database...')
time_end = time.time()
time_start_7d = time_end - (60 * 60 * 24 * 7)
# result_total = mgr_database.db_data_get_all()
result_7d = mgr_database.db_data_get(time_start_7d)
result_1d = result_7d[-86400 * int(1 / k.sensor_reading_frequency):]
print(f'Query Complete.')
print(f'Begin plotting...')

plotter_phaseportrait.wrapper(result_1d)
plotter_spectrograms.wrapper((result_1d))
plotter_combo1day.wrapper(result_1d)
plotter_combo7day.wrapper(result_7d)

timefinish = time.time()
print(f"Plotting complete. Elapsed minutes to process: {(timefinish - time_end) / 60}")


# # =============================================================================================================
# print("Tiltmeter - 24, hourly plots")
# aggregate_array = result_1d
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
# # Convert distance readings to rate of change.
# # This is similar to traditional seismograph display
# dxdt = []
# for i in range(1, len(plot_seismo)):
#     # dx = plot_seismo[i]
#     dx = plot_seismo[i] - plot_seismo[i - 1]
#     dxdt.append(dx)
# plot_utc.pop(0)
#
# avgwindow = 10 * 3
# smoothe_dx = standard_stuff.filter_average(dxdt, avgwindow)
# plot_utc = plot_utc[avgwindow:-avgwindow]
# smoothe_dx = standard_stuff.filter_average(smoothe_dx, avgwindow)
# plot_utc = plot_utc[avgwindow:-avgwindow]
#
# smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
# smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
# smoothe_seismo.pop(0)
#
# ticks = 20
# df = "%d  %H:%M"
# title = "Tiltmeter One Day dx/dt"
# savefolder = k.dir_images
# mgr_matplot.plot_dual_hourly(df, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder)
#
# title = "Phase Plot. "
# savefolder = "phaseimages"
# mgr_matplot.plot_pseudo_phase(df, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder)


# # =============================================================================================================
# # Empirical Mode Decomposition
# print("Empirical Mode Decomposition")
# aggregate_array = result_1d
# aggregate_array.pop(0)
# plot_utc = []
# plot_seismo = []
# wrapperdata = []
#
# for i in range(1, len(aggregate_array)):
#     tim = aggregate_array[i][0]
#     tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
#     siz = aggregate_array[i][1]
#     plot_utc.append(tim)
#     plot_seismo.append(siz)
#
# wrapperdata.append(plot_utc)
# wrapperdata.append(plot_seismo)
# savefile = k.dir_images + os.sep + "imf.png"
# df = "%d  %H:%M"
# mgr_emd.wrapper(wrapperdata, savefile, df)
# # # =============================================================================================================
# # # Statistical analysis to identify events that exceed standrd deviation thresholds, and anything that
# # # triggers strong oscillations at the pendulums fundamental frequency. Display as a 24 hour graph.
# #
# # # =============================================================================================================
# # print("FFT - 1 Days")
# # fft_sevendays.wrapper(result_1d)
# # print("FFT - ALL DATA!!")
# # fft_entire_data.wrapper(result_total)
#
# timefinish = time.time()
# print(f"Elapsed minutes to process: {(timefinish - time_end) / 60}")
