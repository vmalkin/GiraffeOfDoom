import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import standard_stuff
# import os


def plot_time_data(utcdates, pressuredata, readings_per_tick, texttitle, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)

    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    ax.plot(utcdates, pressuredata, c="orange")

    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)

    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M.%f')
    plot_title = texttitle + " (Arbitrary Units) - " + ut

    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)


# def plot_detrended(utc_datelist, pressure_data, readings_per_tick, halfwindow, texttitle, savefile):
#     rawdata = []
#
#     newdatetimes = []
#     newdata = []
#     subarray = []
#
#     # Iterate over data in a single pass to perform rolling average with a window of 2 * halfwindow
#     for i in range(0, len(pressure_data)):
#         utc = utc_datelist[i]
#         pressure = pressure_data[i]
#         if pressure != None:
#             subarray.append(pressure)
#         if len(subarray) >= (2 * halfwindow):
#             average_pressure = np.mean(subarray)
#             newdatetimes.append(utc)
#             # Calculate the detrended data
#             detrended_pressure = pressure - average_pressure
#             newdata.append(detrended_pressure)
#             subarray.pop(0)
#
#     # if os.path.isfile("detrended.csv") is True:
#     #     print("No plotting detrended CSV file")
#     # else:
#     #     with open("detrended.csv", "w") as d:
#     #         for i in range(0, len(newdata)):
#     #             dp = newdatetimes[i] + "," + str(newdata[i]) + "\r\n"
#     #             d.write(dp)
#     #     d.close()
#
#     plt.style.use('Solarize_Light2')
#     fig, ax = plt.subplots(layout="constrained", figsize=(16, 5), dpi=140)
#     ax.plot(newdatetimes, newdata, c="orange")
#     tick_spacing = readings_per_tick
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
#     # ax.set_ylim([-30, 30])
#     plt.xticks(rotation=90)
#     pt = time.time()
#     ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M')
#     plot_title = texttitle + " " + ut
#     ax.set_title(plot_title)
#     # plt.show()
#     plt.savefig(savefile)
#
#     tick_spacing = readings_per_tick
#     ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
#     plt.xticks(rotation=90)
#     pt = time.time()
#     ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M')
#     plot_title = texttitle + ut
#     ax.set_title(plot_title)
#     # plt.show()
#     plt.savefig(savefile)
