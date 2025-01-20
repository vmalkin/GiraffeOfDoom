import time
import matplotlib.pyplot as plt
import numpy as np
import standard_stuff


def plot_time_data(queryresult, savefile):
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

    fig, ax = plt.subplots(layout="constrained", figsize=(16, 10), dpi=140)
    ax.plot(posixtime, signal, c="orange")
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

    fig, ax = plt.subplots(layout="constrained", figsize=(16, 10), dpi=140)
    ax.plot(posixtime, new_dx, c="orange")
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "dx-dt (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)

def plot_detrended(queryresult, halfwindow, savefile):
    rawdata = []
    for item in queryresult:
        pxtm = int(item[0])
        prss = float(item[1])
        d = [pxtm, prss]
        rawdata.append(d)

    datetimes = []
    newdata = []
    if len(rawdata) > 2 * halfwindow + 1:
        for i in range(halfwindow, len(rawdata) - halfwindow):
            avg_press = []

            for j in range(0 - halfwindow, halfwindow):
                avg_press.append(rawdata[i + j][1])

            pxtime = rawdata[i][0]
            pressure = rawdata[i][1]
            pressure_avg = np.mean(avg_press)
            detrend = pressure - pressure_avg

            datetimes.append(standard_stuff.posix2utc(pxtime, '%Y-%m-%d %H:%M:%S'))
            newdata.append(detrend)

    fig, ax = plt.subplots(layout="constrained", figsize=(16, 4), dpi=140)
    ax.plot(datetimes, newdata, c="orange")
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "Detrended Pressure (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)



