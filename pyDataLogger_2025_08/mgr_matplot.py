import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import standard_stuff

ink_colour = ["#7a3f16", "green", "red"]

def plot_multi(dateformatstring, dateobjects, dataarrays, readings_per_tick, texttitle, savefile):
    # utcdates should be datetime objects, not POSIX floats
    plt.style.use('Solarize_Light2')
    fig, ax1 = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    # Subplots with separate y axes
    ax1.plot(dateobjects, dataarrays[0], c=ink_colour[0], linewidth=1)
    ax1.set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
    ax1.tick_params(axis='y', colors=ink_colour[0])
    ax1.set_ylim([451.75, 453])

    ax2 = ax1.twinx()
    ax2.plot(dateobjects, dataarrays[1], c=ink_colour[1], linewidth=1)
    ax2.set_ylabel("Pressure. Pa.", color=ink_colour[1])
    ax2.tick_params(axis='y', colors=ink_colour[1])
    ax2.set_ylim([96000, 102000])
    ax2.spines['right'].set_position(('outward', 60))
    ax2.yaxis.grid(False)

    ax3 = ax1.twinx()
    ax3.plot(dateobjects, dataarrays[2], c=ink_colour[2], linewidth=1)
    ax3.set_ylabel("Temperature. Deg C.", color=ink_colour[2])
    ax3.tick_params(axis='y', colors=ink_colour[2])
    ax3.set_ylim([8, 20])
    ax3.yaxis.grid(False)

    # Use proper date formatter + locator
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax1.get_xticklabels(), rotation=45)  # safer than plt.xticks
    plot_title = texttitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax1.set_title(plot_title)
    plt.savefig(savefile)
    plt.close()


def plot_time_data(dateformatstring, utcdates, maindata, readings_per_tick, ymin, ymax, texttitle, savefile):
    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    # utcdates should be datetime objects, not POSIX floats
    ax.plot(utcdates, maindata, c=ink_colour[0], linewidth=1)
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
    # plt.title(plottitle)
    savefile = savefile
    plt.savefig(savefile)
    plt.close()


def plot_scatterplot(data_x, data_y, plot_title, savefile):
    plt.figure(figsize=(8, 8))
    plt.scatter(data_x, data_y, marker='o')
    plt.title = plot_title
    plt.savefig(savefile)
    plt.close()

