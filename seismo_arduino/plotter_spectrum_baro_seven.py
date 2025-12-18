from datetime import timezone, datetime
import numpy as np
import constants as k
import matplotlib.pyplot as plt
import os
import class_aggregator
import matplotlib.dates as mdates
from scipy.signal import detrend

ink_colour = ["#7a3f16", "blue", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_spectrum(datetimeformat, tickinterval, deltapressure, data, datetimes, plotfrequency, minv, maxv, plottitle, savefile):
    nfft = 16384
    # nfft = 4096
    noverlap = int(nfft * 0.75)
    plt.style.use(plotstyle)

    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(16, 8), dpi=140, sharex=True, height_ratios=[2, 1])
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the .image.AxesImage instance representing the data in the plot
    Pxx, freqs, bins, im = ax_top.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency,
                                         cmap='viridis', vmin=minv, vmax=maxv)
    cbar = fig.colorbar(im, ax=ax_top, pad=0.01)
    cbar.set_label("Power spectral density (dB/Hz)")

    ax_top.set_ylabel("Frequency (Hz) / Period")
    ax_top.set_yscale('log')
    ax_top.set_ylim(10 ** -5.1, 10 ** -1.5)
    # ax_top.set_ylim(freqs[1], freqs[-1])

    subtitle = f" | FFT={nfft}, overlap={noverlap}, Fs={plotfrequency} Hz"
    ax_top.set_title(f"{plottitle}{subtitle}")

    ax_bottom.plot(datetimes, deltapressure, c=ink_colour[1], linewidth=1)
    ax_bottom.set_ylabel("Delta Pressure - Pa.", color=ink_colour[1])
    ax_bottom.tick_params(axis='y', colors=ink_colour[1])
    ax_bottom.yaxis.grid(True)

    # tickplace = []
    # ticklabel = []
    # for i in range(0, len(datetimes), tickinterval):
    #     tickplace.append(i)
    #     ticklabel.append(datetimes[i].strftime(datetimeformat))
    # plt.xticks(ticks=tickplace, labels=ticklabel, rotation=90)

    fig.tight_layout()
    fig.savefig(savefile)
    plt.close(fig)


def get_delta_pressure(plot_press, halfwindow):
    # Return array must be the same length as plot_press, so will be padded with null values at start and end
    novalue = np.nan
    returnarray = []
    endofseries = len(plot_press) - halfwindow
    if len(plot_press) > halfwindow:
        for i in range(0, len(plot_press)):
            if halfwindow < i < endofseries:
                j = plot_press[i + halfwindow] - plot_press[i - halfwindow]
                j = float(round(j, 4))
                returnarray.append(j)
            else:
                returnarray.append(novalue)
    else:
        for item in plot_press:
            returnarray.append(novalue)
    # returnarray.append(novalue)
    return returnarray


def wrapper(data):
    #  spectrographic analysis and filtering improved with ChatGPT
    print("*** Barometric Spectrogram - Past 24 hours")
    window = 10
    aggregate_array = class_aggregator.aggregate_data(window, data)
    aggregate_array.pop(0)

    plot_utc = []
    plot_press = []
    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
        plot_utc.append(tim)
        plot_press.append(prs)

    halfhour = 10 * 60 * 30  # half an hour
    delta_pressure = get_delta_pressure(plot_press, halfhour)

    data = detrend(plot_press, type='linear')
    df = "%d  %H:%M"
    title = "Spectrogram of Barometric Pressure."
    savefile = k.dir_images['images'] + os.sep + "spectrum_press.png"
    tick = 60 * 60 * 12
    # plot_spectrum(df, tick, data, plot_utc, 1, 0, 62, title, savefile)
    plot_spectrum(df, tick, delta_pressure, data, plot_utc, 1, 5, 80, title, savefile)

