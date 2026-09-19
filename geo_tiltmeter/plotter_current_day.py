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


def plot(datetimeformat, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder):
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    hour_slice = k.sensor_reading_frequency * 60 * 60 * 24
    sz_avg = np.mean(smoothe_seismo)
    sz_stdev= np.std(smoothe_seismo)
    sz_ymax = sz_avg + (sz_stdev * 4)
    sz_ymin = sz_avg - (sz_stdev * 4)

    dx_avg = np.mean(smoothe_dx)
    dx_stddev = np.std(smoothe_dx)
    dx_ymax = dx_avg + (dx_stddev * 12)
    dx_ymin = dx_avg - (dx_stddev * 12)

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
        ax[0].set_ylim([sz_ymin, sz_ymax])
        my_fmt = mdates.DateFormatter(datetimeformat)
        ax[0].xaxis.set_major_formatter(my_fmt)
        # Major grid
        ax[0].grid(which='major', linestyle=':', color='black', alpha=1)
        ax[0].grid(which='minor', linestyle=':', color='black',alpha=0.5)
        # Minor ticks and grid
        ax[0].xaxis.set_minor_locator(AutoMinorLocator(6))
        ax[0].yaxis.set_minor_locator(AutoMinorLocator(1))


        # ax[1] = ax1.twinx()
        ax[1].plot(chart_times, diff_data, c=ink_colour[1], linewidth=1)
        ax[1].set_ylabel("Tilt, dx/dt", color=ink_colour[1])
        ax[1].set_ylim([dx_ymin, dx_ymax])
        my_fmt = mdates.DateFormatter(datetimeformat)
        ax[1].xaxis.set_major_formatter(my_fmt)
        # Major grid
        ax[1].grid(which='major', linestyle=':', color='black', alpha=1)
        ax[1].grid(which='minor', linestyle=':', color='black',alpha=0.5)
        # Minor ticks and grid
        ax[1].xaxis.set_minor_locator(AutoMinorLocator(6))
        ax[1].yaxis.set_minor_locator(AutoMinorLocator(1))

        plot_title = title + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
        plt.xlabel("UTC Datetime.")
        fig.suptitle(plot_title)
        savefile = savefolder + os.sep + "current_day.png"
        plt.savefig(savefile)
        plt.close()


def wrapper(utctimes, data):
    # =============================================================================================================
    # Data is UTC time objects and flat data.
    # There may be gaps
    print("*** Tiltmeter current day.")

    smoothing_half_window = k.sensor_reading_frequency * 60
    smooth_seismo = standard_stuff.filter_average(data, smoothing_half_window)
    smooth_times = utctimes[smoothing_half_window:-smoothing_half_window]

    # Create the smoothed dxdt. Remember to pop one value from smooth_utc and smooth_data
    smooth_dxdt = []
    for i in range(1, len(smooth_seismo)):
        j = smooth_seismo[i] - smooth_seismo[i-1]
        smooth_dxdt.append(j)
    smooth_times.pop(0)
    smooth_seismo.pop(0)

    print(f'{len(smooth_times)} {len(smooth_seismo)} {len(smooth_dxdt)}')

    ticks = 20
    df = "%b %d \n%Hhr"
    title = f'Tiltmeter Current Day. Data and dx/dt. RA half-window is {smoothing_half_window} readings @ {k.sensor_reading_frequency} readings/s. '
    savefolder = k.dir_saves['images']

    plot(df,
         smooth_times,
         smooth_seismo,
         smooth_dxdt,
         title,
         savefolder)
