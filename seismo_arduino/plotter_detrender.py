from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import constants as k
import standard_stuff
import class_aggregator


def plot_data(data, dates, filename, dateformatstring):
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    plt.style.use(plotstyle)
    fig, ax = plt.subplots( layout="constrained", figsize=(200, 7), dpi=140)
    title = "Empirical Mode Decomposion - Tilt data. "

    ax.plot(dates, data, c=ink_colour[0], linewidth=1)
    ax.set_ylim([-2, 2])
    # Use proper date formatter + locator
    ax.grid(which='major', axis='x', linestyle='solid', c='black', visible='True', zorder=5)
    ax.grid(which='minor', axis='x', linestyle='dotted', c='black', visible='True', zorder=5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax.xaxis.set_minor_locator(AutoMinorLocator(6))
    plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks

    savefile = filename
    plt.savefig(savefile)
    plt.close()


def wrapper(data):
    print("*** Detrending.")
    # decimate the data
    window = 10
    aggregate_array = class_aggregator.aggregate_data(window, data)
    aggregate_array.pop(0)

    raw_utc = []
    raw_seismo = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
        raw_utc.append(tim)
        raw_seismo.append(siz)


    plot_utc = []
    plot_seismo = []
    readings_per_sec = 1
    # Current detrending by an hour
    detrend_half_window = readings_per_sec * 60 * 5
    end_index = len(raw_seismo) - detrend_half_window

    for i in range(0, len(raw_seismo)):
        if detrend_half_window < i < end_index:
            window_data = raw_seismo[i - detrend_half_window: i + detrend_half_window]
            dd = raw_seismo[i] - np.nanmean(window_data)
            dt = raw_utc[i]
            plot_seismo.append(dd)
            plot_utc.append(dt)
            if i % 100000 == 0:
                print(f'Detrend {int(i / len(raw_seismo) * 100)}% completed...')

    # Some smoothing is required here
    avgwindow = 2
    plot_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]
    plot_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]

    print(f'Detrend completed!')
    df = "%d  %H:%M"
    savefile = k.dir_images['images'] + os.sep + "detrended.png"
    plot_data(plot_seismo, plot_utc, savefile, df)



