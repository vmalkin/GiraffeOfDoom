import os
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import standard_stuff
import numpy as np

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


def plot_spectrum(datetimeformat, tickinterval, data, datetimes, plotfrequency, minv, maxv, plottitle, savefile):
    frequency = 1 / plotfrequency
    plt.figure(layout="constrained", figsize=(15, 6))
    plt.style.use(plotstyle)
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno', vmin=minv, vmax=maxv)
    # Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno')
    # Add colorbar (this is your "legend" for the colors)
    cbar = plt.colorbar(im)
    cbar.set_label('Power / Frequency (dB/Hz)')
    tickplace = []
    ticklabel = []
    for i in range(0, len(datetimes), tickinterval):
        tickplace.append(i)
        ticklabel.append(datetimes[i].strftime(datetimeformat))
    plt.xticks(ticks=tickplace, labels=ticklabel, rotation=90)

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(plottitle)
    savefile = savefile
    plt.savefig(savefile)
    plt.close()


def plot_scatterplot(data_x, data_y, plot_title, savefile):
    plt.figure(figsize=(8, 8))
    plt.style.use(plotstyle)
    plt.scatter(data_x, data_y, marker='o')
    plt.title(plot_title)
    plt.savefig(savefile)
    plt.close()



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


def plot_pseudo_phase(datetimeformat, plot_utc, plot_seismo, dxdt, title, savefolder):
    try_create_directory(savefolder)
    # the size of an hour is plot frequency multiplied by seconds/min and mins/hr
    hour_slice = 10 * 60 * 10
    sz_avg = np.mean(plot_seismo)
    sz_max = max(plot_seismo)
    sz_min = min(plot_seismo)
    xmax = sz_avg + 1.1 * (sz_max - sz_avg)
    xmin = sz_avg - 1.1 * (sz_avg - sz_min)

    dx_avg = np.mean(dxdt)
    dx_max = max(dxdt)
    dx_min = min(dxdt)
    ymax = dx_avg + 1.1 * (dx_max - dx_avg)
    ymin = dx_avg - 1.1 * (dx_avg - dx_min)

    for i in range(0, len(plot_seismo), hour_slice):
        array_start = i
        array_end = i + hour_slice
        seismo_data = plot_seismo[array_start:array_end]
        diff_data = dxdt[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]

        plt.style.use(plotstyle)
        fig, ax = plt.subplots(layout="constrained", figsize=(8, 8), dpi=140)
        ax.set_ylim([ymin, ymax])
        ax.set_xlim([xmin, xmax])
        # utcdates should be datetime objects, not POSIX floats
        ax.scatter(seismo_data, diff_data, c=ink_colour[0], s=3)

        plot_title = title + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
        fig.suptitle(plot_title)
        savefile = savefolder + os.sep + "pp_" + str(i) + ".png"
        plt.savefig(savefile)
        plt.close()