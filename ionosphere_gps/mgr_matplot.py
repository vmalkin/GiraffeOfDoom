import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import standard_stuff
import math

def plot_polar_noise(queryresult, savefile):
    # plt.style.use('_mpl-gallery')
    # Polar plot Theta axis is in radians!
    altitude = []
    azimuth = []
    signalnoise = []
    for item in queryresult:
        try:
            # datetime.append(item[2])
            alt = item[3]
            azi = item[4]
            snr = item[5]
            # print(item)
            if alt == '':
                alt = np.nan
            else:
                alt = int(alt)
                # print("Null altitude value")

            if azi == '':
                azi = np.nan
            else:
                # azimuths have to be in radians, even tho the graph shows them as degrees
                azi = azi * (np.pi / 180)
                # print("Null azimuth value")

            if snr == '':
                snr = np.nan
            else:
                snr = int(snr)
                # print("Null altitude value")

            altitude.append(alt)
            azimuth.append(azi)
            signalnoise.append(snr)
        except:
            print("Error adding item")
    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M')
    plot_title = "12 Hour SNR Tracks - " + ut

    fig = plt.figure(layout="constrained", figsize=(6, 6), dpi=140)
    ax = fig.add_subplot(projection='polar')
    ax.scatter(azimuth, altitude, s=5, c=signalnoise, cmap='Blues', alpha=0.5)
    ax.set_rmax(0)
    ax.set_rmin(90)
    ax.set_theta_zero_location("S")
    ax.set_theta_direction(1)
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)

def plot_time_snr(data_blob, time_array, savefile):
    # [1748287326.1275165, snr, alt]
    fig, ax = plt.subplots(layout="constrained", figsize=(12, 5), dpi=140)

    for data_series in data_blob:
        ax.plot(time_array, data_series)

    tick_spacing = 60 * 60
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=90)

    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M:%S')
    plot_title = "24 Hour SNR - " + ut
    ax.set_title(plot_title)
    plt.savefig(savefile)

