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


def plot_dual_hourly(datetimeformat, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder):
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    hour_slice = k.sensor_reading_frequency * 60 * 15
    # sz_avg = np.nanmean(smoothe_seismo)
    # sz_stdev= np.nanstd(smoothe_seismo)
    # sz_ymax = sz_avg + (sz_stdev * 8)
    # sz_ymin = sz_avg - (sz_stdev * 8)
    #
    # dx_avg = np.nanmean(smoothe_dx)
    # dx_stddev = np.nanstd(smoothe_dx)
    # dx_ymax = dx_avg + (dx_stddev * 12)
    # dx_ymin = dx_avg - (dx_stddev * 12)

    for i in range(0, len(smoothe_seismo), hour_slice):
        array_start = i
        array_end = i + hour_slice
        seismo_data = smoothe_seismo[array_start:array_end]
        diff_data = smoothe_dx[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]

        plt.style.use(plotstyle)
        fig, ax = plt.subplots(2, layout="constrained", figsize=(16, 8), dpi=250)

        # utcdates should be datetime objects, not POSIX floats
        ax[0].plot(chart_times, seismo_data, c=ink_colour[0], linewidth=1)
        ax[0].set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
        # ax[0].set_ylim([sz_ymin, sz_ymax])
        my_fmt = mdates.DateFormatter(datetimeformat)
        ax[0].xaxis.set_major_formatter(my_fmt)
        # Major grid
        ax[0].grid(which='major', linestyle=':', color='black', alpha=1)
        ax[0].grid(which='minor', linestyle=':', color='black',alpha=0.5)
        # Minor ticks and grid
        ax[0].xaxis.set_minor_locator(AutoMinorLocator(5))
        ax[0].yaxis.set_minor_locator(AutoMinorLocator(1))


        # ax[1] = ax1.twinx()
        ax[1].plot(chart_times, diff_data, c=ink_colour[1], linewidth=1)
        ax[1].set_ylabel("Tilt, dx/dt", color=ink_colour[1])
        # ax[1].set_ylim([dx_ymin, dx_ymax])
        my_fmt = mdates.DateFormatter(datetimeformat)
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
        print(f"Dualplotter: {i} / {len(smoothe_seismo)}")


def wrapper(utctimes, data):
    # =============================================================================================================
    # Data is UTC time objects and flat data.
    # There may be gaps
    print("*** Tiltmeter, hourly plots")
    #
    # smoothing_half_window = k.sensor_reading_frequency * 5
    # smooth_seismo = data
    # smooth_times = utctimes

    # Create the smoothed dxdt. Remember to pop one value from smooth_utc and smooth_data
    smooth_dxdt = []
    for i in range(1, len(data)):
        if data[i] is not None:
            if data[i-1] is not None:
                j = data[i] - data[i-1]
                smooth_dxdt.append(j)
    utctimes.pop(0)
    data.pop(0)

    print(f'{len(utctimes)} {len(data)} {len(smooth_dxdt)}')

    ticks = 20
    df = "%b %d \n%H:%M"
    title = f'Tiltmeter One Day. Data and dx/dt.'
    savefolder = k.dir_saves['images']

    plot_dual_hourly(df,
                     utctimes,
                     data,
                     smooth_dxdt,
                     title,
                     savefolder)
