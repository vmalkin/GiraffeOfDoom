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

def plot_helicorder(dateformatstring, plotdates, plotdata, readings_per_tick, texttitle):
    # hour slice depends on plot requency and if any decimation has taken place. IT should be the number of readings
    # that make up an hour
    hour_slice = 60 * 60
    rownum = math.ceil(len(plotdata) / hour_slice)
    plot_height = rownum * 300
    plt.style.use(plotstyle)
    fig, ax = plt.subplots(nrows=rownum,layout="constrained", figsize=(10, 20), dpi=140)

    axindex = 0
    for i in range(0, len(plotdata), hour_slice):
        array_start = i
        array_end = i + hour_slice
        seismo_data = plotdata[array_start:array_end]
        chart_times = plotdates[array_start:array_end]

        # Subplots with separate y axes
        ax[axindex].plot(chart_times, seismo_data, c=ink_colour[0], linewidth=1)
        # ax[axindex].set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
        ax[axindex].tick_params(axis='y', colors=ink_colour[0])

        avgv = np.mean(plotdata)
        maxv = max(plotdata)
        minv = min(plotdata)
        ymax = avgv + 2 * (maxv - avgv)
        ymin = avgv - 2 * (avgv - minv)

        ax[axindex].set_ylim([ymin, ymax])
        #
        # ax2 = ax1.twinx()
        # ax2.plot(dateobjects, dataarrays[1], c=ink_colour[1], linewidth=2)
        # ax2.set_ylabel("Pressure. Pa.", color=ink_colour[1])
        # ax2.tick_params(axis='y', colors=ink_colour[1])
        # maxv = max(dataarrays[1])
        # minv = min(dataarrays[1])
        # ax2.set_ylim([minv, maxv])
        # ax2.spines['right'].set_position(('outward', 60))
        # ax[axindex].yaxis.grid(False)
        #
        # ax3 = ax1.twinx()
        # ax3.plot(dateobjects, dataarrays[2], c=ink_colour[2], linewidth=2)
        # ax3.set_ylabel("Temperature. Deg C.", color=ink_colour[2])
        # ax3.tick_params(axis='y', colors=ink_colour[2])
        # # maxv = 18
        # # minv = 8
        # maxv = max(dataarrays[2])
        # minv = min(dataarrays[2])
        # ax3.set_ylim([minv, maxv])
        # ax3.yaxis.grid(False)
        #
        # Use proper date formatter + locator

        # plt.savefig(savefile)
        # plt.close()
        axindex = axindex + 1
    # ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    # ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    # plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks
    # plot_title = texttitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    # ax.set_title(plot_title)
    plt.show()



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

    ticks = 20
    df = "%d  %H:%M"
    title = "Tiltmeter One Day"
    savefile = "images" + os.sep + "helicorder.png"
    plot_helicorder(df, plot_utc, plot_dxdt, ticks, title)