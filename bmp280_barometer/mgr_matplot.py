import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import standard_stuff


def plot_time_data(queryresult, decimation, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)
    posixtime = []
    signal = []

    for i in range(0, len(queryresult), decimation):
        psx = queryresult[i][0]
        sgn = queryresult[i][1]

        if psx == '':
            psx = np.nan
        else:
            psx = standard_stuff.posix2utc(psx, '%H:%M:%S')
            # psx = int(psx)

        if sgn == '':
            sgn = np.nan
        else:
            sgn = float(sgn)

        posixtime.append(psx)
        signal.append(sgn)

    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    plt.style.context('Solarize_Light2')
    ax.plot(posixtime, signal, c="orange")
    tick_spacing = 60
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "Barometric Pressure (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)


def plot_time_dxdt(queryresult, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)
    posixtime = []
    signal = []

    for item in queryresult:
        psx = item[0]
        sgn = item[1]

        if psx == '':
            psx = np.nan
        else:
            psx = standard_stuff.posix2utc(psx, '%H:%M:%S')
            # psx = int(psx)

        if sgn == '':
            sgn = np.nan
        else:
            sgn = float(sgn)

        posixtime.append(psx)
        signal.append(sgn)

    dx = []
    for i in range(1, len(signal)):
        d = signal[i] - signal[i - 1]
        dx.append(d)

    filterwindow = 20
    posixtime = posixtime[(filterwindow * 2) + 1:]
    new_dx = standard_stuff.filter_average(dx, filterwindow)


    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    plt.style.context('Solarize_Light2')
    ax.plot(posixtime, new_dx, c="orange")
    tick_spacing = 60
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "dx-dt (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)

def plot_detrended(queryresult, decimation, halfwindow, savefile):
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


    fig, ax = plt.subplots(layout="constrained", figsize=(16, 5), dpi=140)
    ax.plot(newdatetimes, newdata, c="orange")
    tick_spacing = 60
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "Detrended Pressure (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)



