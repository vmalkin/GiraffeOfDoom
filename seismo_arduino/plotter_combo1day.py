from datetime import timezone, datetime
import standard_stuff
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
import constants as k

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

def plot_multi(dateformatstring, dateobjects, dataarrays, readings_per_tick, texttitle, savefile):
    # utcdates should be datetime objects, not POSIX floats
    plt.style.use(plotstyle)
    fig, ax1 = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    # Subplots with separate y axes
    ax1.plot(dateobjects, dataarrays[0], c=ink_colour[0], linewidth=1)
    ax1.set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
    ax1.tick_params(axis='y', colors=ink_colour[0])

    avgv = np.mean(dataarrays[0])
    maxv = max(dataarrays[0])
    minv = min(dataarrays[0])
    ymax = avgv + 2 * (maxv - avgv)
    ymin = avgv - 2 * (avgv - minv)
    ax1.set_ylim([ymin, ymax])

    ax2 = ax1.twinx()
    ax2.plot(dateobjects, dataarrays[1], c=ink_colour[1], linewidth=1)
    ax2.set_ylabel("Pressure. Pa.", color=ink_colour[1])
    ax2.tick_params(axis='y', colors=ink_colour[1])
    maxv = max(dataarrays[1])
    minv = min(dataarrays[1])
    ax2.set_ylim([minv, maxv])
    ax2.spines['right'].set_position(('outward', 60))
    ax2.yaxis.grid(False)

    ax3 = ax1.twinx()
    ax3.plot(dateobjects, dataarrays[2], c=ink_colour[2], linewidth=1)
    ax3.set_ylabel("Temperature. Deg C.", color=ink_colour[2])
    ax3.tick_params(axis='y', colors=ink_colour[2])
    # maxv = 18
    # minv = 8
    maxv = max(dataarrays[2])
    minv = min(dataarrays[2])
    ax3.set_ylim([minv, maxv])
    ax3.yaxis.grid(False)

    # Use proper date formatter + locator
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax1.get_xticklabels(), rotation=90)  # safer than plt.xticks
    plot_title = texttitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax1.set_title(plot_title)
    plt.savefig(savefile)
    plt.close()


def wrapper(data):
    # =============================================================================================================
    print("Tilt, Temp, Barometer - 1 Day")
    aggregate_array = data
    aggregate_array.pop(0)
    plot_utc = []
    plot_seismo = []
    plot_temp = []
    plot_press = []
    wrapper = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i][1]
        tmp = aggregate_array[i][2]
        prs = aggregate_array[i][3]
        plot_utc.append(tim)
        plot_seismo.append(siz)
        plot_temp.append(tmp)
        plot_press.append(prs)

    avgwindow = 20
    smoothe_seismo = standard_stuff.filter_average(plot_seismo, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]
    plot_temp = plot_temp[avgwindow:-avgwindow]
    plot_press = plot_press[avgwindow:-avgwindow]
    smoothe_seismo = standard_stuff.filter_average(smoothe_seismo, avgwindow)
    plot_utc = plot_utc[avgwindow:-avgwindow]
    plot_temp = plot_temp[avgwindow:-avgwindow]
    plot_press = plot_press[avgwindow:-avgwindow]
    wrapper.append(smoothe_seismo)
    wrapper.append(plot_press)
    wrapper.append(plot_temp)

    ticks = 20
    df = "%d  %H:%M"
    title = "Tiltmeter One Day"
    savefile = k.dir_images + os.sep + "one_day.png"
    plot_multi(df, plot_utc, wrapper, ticks, title, savefile)
