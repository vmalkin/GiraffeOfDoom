from datetime import timezone, datetime
import time
import standard_stuff
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import constants as k
import class_aggregator
import math

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")

def plot_helicorder(dateformatstring, plotdates, plotdata, readings_per_tick, texttitle, savefile):
    # hour slice depends on plot requency and if any decimation has taken place. IT should be the number of readings
    # that make up an hour
    hour_slice = 60 * 60
    rownum = math.ceil(len(plotdata) / hour_slice)
    plt.style.use(plotstyle)
    fig, ax = plt.subplots(nrows=rownum, figsize=(10, 1.4 * rownum), dpi=140)
    fig.set_constrained_layout(True)

    avgv = np.mean(plotdata)
    maxv = max(plotdata)
    minv = min(plotdata)
    ymax = avgv + (1.1 * (maxv - avgv))
    ymin = avgv - (1.1 * (avgv - minv))
    plot_title = texttitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    fig.suptitle(plot_title)

    axindex = 0
    for i in range(0, len(plotdata), hour_slice):
        array_start = i
        array_end = i + hour_slice
        seismo_data = plotdata[array_start:array_end]
        chart_times = plotdates[array_start:array_end]
        ax[axindex].plot(chart_times, seismo_data, c=ink_colour[0], linewidth=0.5)
        ax[axindex].set_ylim([ymin, ymax])
        ax[axindex].xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
        ax[axindex].xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
        ax[axindex].xaxis.set_minor_locator(mdates.MinuteLocator(interval=1))
        ax[axindex].grid(which='minor', axis='x', linestyle=':', linewidth=0.5)
        ax[axindex].set_yticklabels([])
        axindex = axindex + 1
    # finally save and close!
    plt.savefig(savefile)
    plt.close()



def wrapper(data):
    print("Helicorder - 1 Day")
    # decimate data for this. Window is the counted in samples, not seconds
    # decimate to one second
    window = 10
    aggregate_array = class_aggregator.aggregate_data(window, data)

    plot_utc = []
    plot_dxdt = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        dt1 = aggregate_array[i - 1].get_data_avg(aggregate_array[i - 1].data_seismo)
        # We have to catch any nulls that are in our data - they can happen
        if dt1 is not None:
            dt2 = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
            if dt2 is not None:
                dt = dt2 - dt1
                plot_utc.append(tim)
                plot_dxdt.append(dt)

    # Some smoothing is required here
    avgwindow = 10
    smoothe_dx = standard_stuff.filter_average(plot_dxdt, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]
    smoothe_dx = standard_stuff.filter_average(smoothe_dx, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]

    ticks = 10
    df = "%d  %H:%M"
    title = "Helicorder One Day"
    savefile = "images" + os.sep + "helicorder.png"
    plot_helicorder(df, plot_utc, smoothe_dx, ticks, title, savefile)