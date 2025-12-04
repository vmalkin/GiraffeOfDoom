from datetime import timezone, datetime
import standard_stuff
import matplotlib.pyplot as plt
import numpy as np
import os
import constants as k

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_pseudo_phase(datetimeformat, plot_utc, plot_seismo, dxdt, title, savefolder):
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    hour_slice = 10 * 60 * 10
    sz_avg = np.mean(plot_seismo)
    sz_max = np.nanmax(plot_seismo)
    sz_min = np.nanmin(plot_seismo)
    xmax = sz_avg + 1.1 * (sz_max - sz_avg)
    xmin = sz_avg - 1.1 * (sz_avg - sz_min)

    dx_avg = np.mean(dxdt)
    dx_max = np.nanmax(dxdt)
    dx_min = np.nanmin(dxdt)
    ymax = dx_avg + 1.1 * (dx_max - dx_avg)
    ymin = dx_avg - 1.1 * (dx_avg - dx_min)

    for i in range(0, len(plot_seismo), hour_slice):
        array_start = i
        array_end = i + hour_slice
        seismo_data = plot_seismo[array_start:array_end]
        diff_data = dxdt[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]
        begintime = chart_times[0].strftime(datetimeformat)
        endtime = chart_times[len(chart_times) - 1].strftime(datetimeformat)

        plt.style.use(plotstyle)
        fig, ax = plt.subplots(layout="constrained", figsize=(8, 8), dpi=140)
        ax.set_ylim([ymin, ymax])
        ax.set_xlim([xmin, xmax])
        # utcdates should be datetime objects, not POSIX floats
        # ax.scatter(seismo_data, diff_data, c=ink_colour[0], s=3)
        ax.plot(seismo_data, diff_data, c=ink_colour[0], linewidth=1)

        plot_title = title + " - " + begintime + " - " + endtime
        fig.suptitle(plot_title)
        savefile = savefolder + os.sep + "pp_" + str(i) + ".png"
        plt.savefig(savefile)
        plt.close()


def wrapper(data):
    print("Phase Plots.")
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
    title = "Phase Plot. "
    savefolder = k.dir_images['phaseplots']
    # try_create_directory(savefolder)
    plot_pseudo_phase(df, plot_utc, smoothe_seismo, smoothe_dx, title, savefolder)
