import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import numpy as np
import standard_stuff
import os

ink_colour = "#7a3f16"

def plot_time_data(dateformatstring, utcdates, maindata, readings_per_tick, ymin, ymax, texttitle, savefile):
    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)

    # utcdates should be datetime objects, not POSIX floats
    ax.plot(utcdates, maindata, c=ink_colour, linewidth=1)

    # Use proper date formatter + locator
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))

    plt.setp(ax.get_xticklabels(), rotation=45)  # safer than plt.xticks
    ax.set_ylim([ymin, ymax])

    plot_title = texttitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax.set_title(plot_title)

    plt.savefig(savefile)
    plt.close()


def plot_spectrum(datetimeformat, data, datetimes, plotfrequency, minv, maxv, plottitle, savefile):
    frequency = 1 / plotfrequency

    plt.figure(layout="constrained", figsize=(15, 5))
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno', vmin=minv, vmax=maxv)
    # Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno')
    # Add colorbar (this is your "legend" for the colors)
    cbar = plt.colorbar(im)
    cbar.set_label('Power / Frequency (dB/Hz)')
    tickplace = []
    ticklabel = []
    for i in range(0, len(datetimes), 60*60):
        tickplace.append(i)
        ticklabel.append(datetimes[i])
    plt.xticks(ticks=tickplace, labels=ticklabel, rotation=45)

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(plottitle)
    savefile = savefile
    plt.savefig(savefile)
    plt.close()


def plot_scatterplot(data_x, data_y, plot_title, savefile):
    plt.figure(figsize=(8, 8))
    plt.scatter(data_x, data_y, marker='o')
    plt.title = plot_title
    plt.savefig(savefile)
    plt.close()

