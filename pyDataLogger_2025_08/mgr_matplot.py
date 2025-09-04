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
    ax.plot(utcdates, maindata, c=ink_colour, linewidth=1)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d %H:%M"))
    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(rotation=45)

    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M')
    plot_title = texttitle + " - " + ut
    ax.set_ylim([ymin, ymax])
    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)
    plt.close()


# def plot_hourly_array(utcdates, sensor_data, save_path):
#     # Data is about 5 readings per second. Calculate how many readings for an hour
#     window = 5 * 60 * 60
#     index_start = 0
#     index_end = window
#
#     for i in range(0, 50):
#         hour_data = sensor_data[index_start: index_end]
#         hour_utc = utcdates[index_start: index_end]
#         try:
#             plt.style.use('Solarize_Light2')
#             fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
#             ax.plot(hour_utc, hour_data, c=ink_colour, linewidth=1)
#             ax.xaxis.set_major_locator(ticker.MultipleLocator(3000))
#             ax.set_ylim([400, 500])
#             # ax.set_xlim([0, 0.3])
#             plt.xticks(rotation=45)
#
#             pt = time.time()
#             ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M.%f')
#             texttitle = hour_data[0]
#             plot_title = str(texttitle) + " (Arbitrary Units) - " + ut
#             savefile = save_path + os.sep + f"{i:03}" + ".png"
#             ax.set_title(plot_title)
#             plt.savefig(savefile)
#             # increment the indices for slicing the array
#             index_start = index_end
#             index_end = index_end + window
#             plt.close()
#         except:
#             print("Finished")


def plot_spectrum(data, datetimes, plotfrequency, minv, maxv, plottitle, savefile):
    frequency = 1 / plotfrequency

    plt.figure(layout="constrained", figsize=(15, 5))
    # Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno', vmin=minv, vmax=maxv)
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno')
    # Add colorbar (this is your "legend" for the colors)
    cbar = plt.colorbar(im)
    cbar.set_label('Power / Frequency (dB/Hz)')
    # plt.specgram(data)
    # print("Pxx shape:", Pxx.shape)
    # print("Frequency bins:", freqs.shape)
    # print("Time bins:", bins.shape)
    # print("Pxx min/max:", Pxx.min(), "/", Pxx.max())
    # print("Pxx sample (dB):", 10 * np.log10(Pxx[0:3, 0:5]))  # Convert to dB to match what you see in the image
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

