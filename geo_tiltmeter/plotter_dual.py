# from datetime import timezone, datetime
import time
import standard_stuff
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates
import numpy as np
import os
import constants as k

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_dual_hourly(
        df,
        utctimes,
        data,
        data_dx,
        title,
        savefolder
    ):
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    hour_slice = (k.datapersecond * 60) * 30
    sz_avg = np.nanmean(data)
    # Use the RMS for the margin
    margin = np.sqrt(np.mean(np.square(data))) * 6
    sz_ymax = sz_avg + margin
    sz_ymin = sz_avg - margin

    dx_avg = np.nanmean(data_dx)
    # Use the RMS for the margin
    margin = np.sqrt(np.mean(np.square(data))) * 0.3
    dx_ymax = dx_avg + margin
    dx_ymin = dx_avg - margin

    for i in range(0, len(data), hour_slice):
        print(f'Dual Plots {i} / {len(data)}')
        array_start = i
        array_end = i + hour_slice
        seismo = data[array_start:array_end]
        dx = data_dx[array_start:array_end]
        chart_times = utctimes[array_start:array_end]

        plt.style.use(plotstyle)
        fig, ax = plt.subplots(2, layout="constrained", figsize=(16, 8), dpi=250)

        # utcdates should be datetime objects, not POSIX floats
        ax[0].plot(chart_times, seismo, c=ink_colour[0], linewidth=1)
        ax[0].set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
        ax[0].set_ylim([sz_ymin, sz_ymax])
        my_fmt = mdates.DateFormatter(df)
        ax[0].xaxis.set_major_formatter(my_fmt)
        # Major grid
        ax[0].grid(which='major', linestyle=':', color='black', alpha=1)
        ax[0].grid(which='minor', linestyle=':', color='black',alpha=0.5)
        # Minor ticks and grid
        ax[0].xaxis.set_minor_locator(AutoMinorLocator(5))
        ax[0].yaxis.set_minor_locator(AutoMinorLocator(1))

        # ax[1] = ax1.twinx()
        ax[1].plot(chart_times, dx, c=ink_colour[1], linewidth=1)
        ax[1].set_ylabel("Tilt, dx/dt", color=ink_colour[1])
        ax[1].set_ylim([dx_ymin, dx_ymax])
        my_fmt = mdates.DateFormatter(df)
        ax[1].xaxis.set_major_formatter(my_fmt)
        # Major grid
        ax[1].grid(which='major', linestyle=':', color='black', alpha=1)
        ax[1].grid(which='minor', linestyle=':', color='black',alpha=0.5)
        # Minor ticks and grid
        ax[1].xaxis.set_minor_locator(AutoMinorLocator(5))
        ax[1].yaxis.set_minor_locator(AutoMinorLocator(1))

        plot_title = title + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
        plt.xlabel("UTC Datetime.")
        fig.suptitle(plot_title)
        savefile = savefolder + os.sep + str(i) + ".png"
        plt.savefig(savefile)
        plt.close()
        # print(f"Dualplotter: {i} / {len(smoothe_seismo)}")


def wrapper(utctimes,
            data,
            data_dx):

    print("*** Tiltmeter, hourly plots")
    ticks = 20
    df = "%b %d \n%H:%M"
    title = f'Tiltmeter One Day. Data and dx/dt.'
    savefolder = k.dir_saves['images']
    plot_dual_hourly(
        df=df,
        utctimes=utctimes,
        data=data,
        data_dx=data_dx,
        title=title,
        savefolder=savefolder
    )
