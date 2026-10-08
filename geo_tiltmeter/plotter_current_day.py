# from datetime import timezone, datetime
import time
import standard_stuff
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates
import numpy as np
import os
import constants as k

ink_colour = ["#7a3f16", "red", "blue", "#ffffff"]
plotstyle = 'bmh'


def plot(df,
         utctimes,
         data,
         temperature,
         pressure,
         title,
         savefile):
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    # hour_slice = k.datapersecond * 60 * 60 * 24
    # sz_avg = np.mean(smoothe_seismo)
    # sz_stdev= np.std(smoothe_seismo)
    # sz_ymax = sz_avg + (sz_stdev * 3)
    # sz_ymin = sz_avg - (sz_stdev * 3)
    #
    # dx_avg = np.mean(smoothe_dx)
    # dx_stddev = np.std(smoothe_dx)
    # dx_ymax = dx_avg + (dx_stddev * 5)
    # dx_ymin = dx_avg - (dx_stddev * 5)
    # print(dx_avg, dx_stddev)

    # for i in range(0, len(smoothe_seismo), hour_slice):
    #     array_start = i
    #     array_end = i + hour_slice
    #     seismo_data = smoothe_seismo[array_start:array_end]
    #     diff_data = smoothe_dx[array_start:array_end]
    #     chart_times = plot_utc[array_start:array_end]

    plt.style.use(plotstyle)
    fig, ax = plt.subplots(3, layout="constrained", figsize=(8, 11), dpi=250)

    # utcdates should be datetime objects, not POSIX floats
    ax[0].plot(utctimes, data, c=ink_colour[0], linewidth=1)
    ax[0].set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
    # ax[0].set_ylim([sz_ymin, sz_ymax])
    my_fmt = mdates.DateFormatter(df)
    ax[0].xaxis.set_major_formatter(my_fmt)
    # Major grid
    ax[0].grid(which='major', linestyle=':', color='black', alpha=1)
    ax[0].grid(which='minor', linestyle=':', color='black',alpha=0.5)
    # Minor ticks and grid
    ax[0].xaxis.set_minor_locator(AutoMinorLocator(6))
    ax[0].yaxis.set_minor_locator(AutoMinorLocator(1))


    # ax[1] = ax1.twinx()
    ax[1].plot(utctimes, temperature, c=ink_colour[1], linewidth=1)
    ax[1].set_ylabel("Tilt, dx/dt", color=ink_colour[1])
    # ax[1].set_ylim([dx_ymin, dx_ymax])
    my_fmt = mdates.DateFormatter(df)
    ax[1].xaxis.set_major_formatter(my_fmt)
    # Major grid
    ax[1].grid(which='major', linestyle=':', color='black', alpha=1)
    ax[1].grid(which='minor', linestyle=':', color='black',alpha=0.5)
    # Minor ticks and grid
    ax[1].xaxis.set_minor_locator(AutoMinorLocator(6))
    ax[1].yaxis.set_minor_locator(AutoMinorLocator(1))

    # ax[1] = ax1.twinx()
    ax[2].plot(utctimes, pressure, c=ink_colour[2], linewidth=1)
    ax[2].set_ylabel("Tilt, dx/dt", color=ink_colour[2])
    # ax[2].set_ylim([dx_ymin, dx_ymax])
    my_fmt = mdates.DateFormatter(df)
    ax[2].xaxis.set_major_formatter(my_fmt)
    # Major grid
    ax[2].grid(which='major', linestyle=':', color='black', alpha=1)
    ax[2].grid(which='minor', linestyle=':', color='black',alpha=0.5)
    # Minor ticks and grid
    ax[2].xaxis.set_minor_locator(AutoMinorLocator(6))
    ax[2].yaxis.set_minor_locator(AutoMinorLocator(1))

    plot_title = title + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    plt.xlabel("UTC Datetime.")
    fig.suptitle(plot_title)
    plt.savefig(savefile)
    plt.close()


def wrapper(utctimes, data, temperature, pressure,title, filename):
    # plots tilt, temp and pressure in a single graph.
    # Data is UTC time objects and flat data.
    # There may be gaps
    print(f"*** Tiltmeter plot: {filename}")
    ticks = 20
    df = "%b %d \n%Hhr"
    savefolder = k.dir_saves['images'] + os.sep + filename

    plot(df,
         utctimes,
         data,
         temperature,
         pressure,
         title,
         savefolder)
