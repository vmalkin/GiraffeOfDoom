from datetime import timezone, datetime
import time
import standard_stuff
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import constants as k
import class_aggregator

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_dual_hourly(datetimeformat, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder):
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    hour_slice = 10 * 60 * 10
    sz_avg = np.mean(smoothe_seismo)
    sz_max = max(smoothe_seismo)
    sz_min = min(smoothe_seismo)
    sz_ymax = sz_avg + 1.1 * (sz_max - sz_avg)
    sz_ymin = sz_avg - 1.1 * (sz_avg - sz_min)

    dx_avg = np.mean(smoothe_dx)
    dx_max = max(smoothe_dx)
    dx_min = min(smoothe_dx)
    dx_ymax = dx_avg + 1.1 * (dx_max - dx_avg)
    dx_ymin = dx_avg - 1.1 * (dx_avg - dx_min)

    for i in range(0, len(smoothe_seismo), hour_slice):
        array_start = i
        array_end = i + hour_slice
        seismo_data = smoothe_seismo[array_start:array_end]
        diff_data = smoothe_dx[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]

        plt.style.use(plotstyle)
        fig, ax = plt.subplots(2, layout="constrained", figsize=(16, 8), dpi=140)
        # utcdates should be datetime objects, not POSIX floats
        ax[0].plot(chart_times, seismo_data, c=ink_colour[0], linewidth=1)
        # Subplots with separate y axes
        ax[0].set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
        ax[0].tick_params(axis='y', colors=ink_colour[0])
        ax[0].set_ylim([sz_ymin, sz_ymax])

        # ax[1] = ax1.twinx()
        ax[1].plot(chart_times, diff_data, c=ink_colour[1], linewidth=1)
        ax[1].set_ylabel("Tilt, dx/dt", color=ink_colour[1])
        ax[1].tick_params(axis='y', colors=ink_colour[1])
        ax[1].set_ylim([dx_ymin, dx_ymax])
        # ax[1].spines['right'].set_position(('outward', 30))
        ax[1].yaxis.grid(False)


        plot_title = title + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
        fig.suptitle(plot_title)
        savefile = savefolder + os.sep + str(i) + ".png"
        plt.savefig(savefile)
        plt.close()


def wrapper(data):
    # =============================================================================================================
    print("Tiltmeter - 24, hourly plots")
    aggregate_array = data
    aggregate_array.pop(0)
    plot_utc = []
    plot_seismo = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i][1]
        plot_utc.append(tim)
        plot_seismo.append(siz)

    # Convert distance readings to rate of change.
    # This is similar to traditional seismograph display
    dxdt = []
    for i in range(1, len(plot_seismo)):
        # dx = plot_seismo[i]
        dx = plot_seismo[i] - plot_seismo[i - 1]
        dxdt.append(dx)
    plot_utc.pop(0)

    avgwindow = 10 * 3
    smoothe_dx = standard_stuff.filter_average(dxdt, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]
    smoothe_dx = standard_stuff.filter_average(smoothe_dx, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]

    smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
    smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
    smoothe_seismo.pop(0)

    ticks = 20
    df = "%d  %H:%M"
    title = "Tiltmeter One Day dx/dt"
    savefolder = k.dir_images['images']
    plot_dual_hourly(df, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder)
