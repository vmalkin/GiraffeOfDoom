from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import constants as k


def plot_data(data, dates, filename, dateformatstring):
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'

    plt.style.use(plotstyle)

    fig, ax = plt.subplots( layout="constrained", figsize=(14, 7), dpi=140)
    title = "Empirical Mode Decomposion - Tilt data. "

    ax.plot(dates, data, c=ink_colour[0], linewidth=1)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax.grid(which='major', axis='x', linestyle='solid', c='black', visible='True', zorder=5)
    ax.grid(which='minor', axis='x', linestyle='dotted', c='black', visible='True', zorder=5)

    # Use proper date formatter + locator
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=4))
    plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks

    savefile = filename
    plt.savefig(savefile)
    plt.close()


def wrapper(data):
    print("*** Detrending.")
    aggregate_array = data
    data_utc = []
    data_seismo = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i][1]
        data_utc.append(tim)
        data_seismo.append(siz)

    plot_utc = []
    plot_seismo = []
    readings_per_sec = 10
    detrend_half_window = readings_per_sec * 60 * 5
    end_index = len(data_seismo) - detrend_half_window

    for i in range(0, len(data_seismo)):
        if detrend_half_window < i < end_index:
            window_data = data_seismo[i - detrend_half_window: i + detrend_half_window]
            dd = data_seismo[i] - np.nanmean(window_data)
            dt = data_utc[i]
            plot_seismo.append(dd)
            plot_utc.append(dt)
            if i % 100 == 0:
                print(f'{i} / {len(data_seismo)}')
    df = "%d  %H:%M"
    savefile = k.dir_images['images'] + os.sep + "detrended.png"
    plot_data(plot_seismo, plot_utc, savefile, df)



