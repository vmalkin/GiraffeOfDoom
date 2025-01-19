import time
import matplotlib.pyplot as plt
import numpy as np
import standard_stuff


def plot_time_snr(queryresult, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)
    posixtime = []
    signalnoise = []

    for item in queryresult:
        psx = item[0]
        snr = item[1]

        if psx == '':
            psx = np.nan
        else:
            psx = standard_stuff.posix2utc(psx, '%H:%M:%S')
            # psx = int(psx)

        if snr == '':
            snr = np.nan
        else:
            snr = int(snr)

        posixtime.append(psx)
        signalnoise.append(snr)

    fig, ax = plt.subplots(layout="constrained", figsize=(10, 3), dpi=140)
    ax.plot(posixtime, signalnoise, c="orange")
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "Barometric Pressure (Pascals) - " + ut
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)

