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

    fig, ax = plt.subplots(layout="constrained", figsize=(10, 3), dpi=140)
    ax.plot(posixtime, signal, c="orange")
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "Barometric Pressure (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)

