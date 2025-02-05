import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import standard_stuff
# import os


def plot_time_data(queryresult, decimation, readings_per_tick, texttitle, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)
    posixtime = []
    signal = []

    for i in range(0, len(queryresult), decimation):
        psx = queryresult[i][0]
        sgn = queryresult[i][1]

        if psx == '':
            psx = np.nan
        else:
            psx = standard_stuff.posix2utc(psx, '%Y-%m-%d %H:%M')
            # psx = int(psx)

        if sgn == '':
            sgn = np.nan
        else:
            sgn = float(sgn)

        posixtime.append(psx)
        signal.append(sgn)

    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    ax.plot(posixtime, signal, c="orange")

    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)

    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M')
    plot_title = texttitle + " (Pascals) - " + ut

    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)


def plot_detrended(queryresult, decimation, readings_per_tick, halfwindow, texttitle, savefile):
    rawdata = []
    for item in queryresult:
        pxtm = int(item[0])
        prss = float(item[1])
        d = [pxtm, prss]
        rawdata.append(d)

    newdatetimes = []
    newdata = []
    subarray = []

    # Iterate over data in a single pass to perform rolling average with a window of 2 * halfwindow
    for i in range(0, len(rawdata), decimation):
        utc = standard_stuff.posix2utc(rawdata[i][0], '%Y-%m-%d %H:%M:%S')
        pressure = rawdata[i][1]
        subarray.append(pressure)
        if len(subarray) >= (2 * halfwindow):
            average_pressure = np.mean(subarray)
            newdatetimes.append(utc)
            # Calculate the detrended data
            detrended_pressure = pressure - average_pressure
            newdata.append(detrended_pressure)
            subarray.pop(0)

    # if os.path.isfile("detrended.csv") is True:
    #     print("No plotting detrended CSV file")
    # else:
    #     with open("detrended.csv", "w") as d:
    #         for i in range(0, len(newdata)):
    #             dp = newdatetimes[i] + "," + str(newdata[i]) + "\r\n"
    #             d.write(dp)
    #     d.close()

    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 5), dpi=140)
    ax.plot(newdatetimes, newdata, c="orange")
    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # ax.set_ylim([-30, 30])
    plt.xticks(rotation=90)
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = texttitle + " " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)


def plot_stats(queryresult, decimation, readings_per_tick, halfwindow, savefile):
    rawdata = []
    for item in queryresult:
        pxtm = int(item[0])
        prss = float(item[1])
        d = [pxtm, prss]
        rawdata.append(d)

    newdatetimes = []
    data_stdev = []
    subarray = []

    # Iterate over data in a single pass to perform rolling average with a window of 2 * halfwindow
    for i in range(0, len(rawdata), decimation):
        utc = standard_stuff.posix2utc(rawdata[i][0], '%Y-%m-%d %H:%M:%S')
        pressure = rawdata[i][1]
        subarray.append(pressure)
        if len(subarray) >= (2 * halfwindow):
            d_stdev = np.std(subarray)
            data_stdev.append(d_stdev)
            newdatetimes.append(utc)
            subarray.pop(0)
    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 5), dpi=140)
    ax.plot(newdatetimes, data_stdev, c="green")

    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "Standard Deviation (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)
