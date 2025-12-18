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

    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(16, 8), dpi=140, sharex=True, height_ratios=[2, 1])
    spectrum, freqs, t, im = ax_top.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency,
                                         cmap='viridis', vmin=minv, vmax=maxv)
    plt.style.use(plotstyle)
    # # Pxx, freqs, bins, im = plt.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency, cmap='inferno', vmin=minv, vmax=maxv)
    # cbar = ax[0].set_colorbars(im)
    # cbar.set_label('Power / Frequency (dB/Hz)')

    # seis_pos_x = 0
    # seis_pos_y = 10 ** -2
    # ax_top.annotate("1–15 min\nGravity waves, local turbulence.", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
    #              bbox=dict(boxstyle="round", fc="1", color='black'))
    # seis_pos_x = 0
    # seis_pos_y = 10 ** -3
    # ax_top.annotate("15 min–3 hr\nMesoscale pressure variability.", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
    #              bbox=dict(boxstyle="round", fc="1", color='black'))
    # seis_pos_x = 0
    # seis_pos_y = 10 ** -4
    # ax_top.annotate(">3 h\nSynoptic-scale & diurnal variability.", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
    #              bbox=dict(boxstyle="round", fc="1", color='black'))
    # liney = 1.16 * 10 ** -5
    # ax_top.axhline(y=liney, linestyle='dotted', color='cyan')
    # ax_top.text(0, liney, '24 h (diurnal atmospheric tide)', color='cyan')

    # ax[0].set_xlabel("dd hh:mm - UTC")
    ax_top.set_ylabel("Frequency (Hz) / Period")
    ax_top.set_yscale('log')
    ax_top.set_ylim(10 ** -5.1, 10 ** -1.5)

    subtitle = ' FFT = ' + str(nfft) + '. FFT Overlap = ' +str(noverlap) + '. Freq = ' + str(plotfrequency) + 'Hz.'
    plottitle = plottitle + subtitle
    ax_top.set_title(plottitle)

    ax_bottom.plot(datetimes, deltapressure, c=ink_colour[1], linewidth=1)
    # ax_bottom.set_ylabel("Delta Pressure - Pa.", color=ink_colour[1])
    # ax_bottom.tick_params(axis='y', colors=ink_colour[1])
    # ax_bottom.yaxis.grid(True)
    #
    # ax_top.xaxis.set_major_formatter(mdates.DateFormatter(datetimeformat))
    # ax_top.xaxis.set_major_locator(mdates.MinuteLocator(interval=tickinterval))
    # plt.setp(ax_bottom.get_xticklabels(), rotation=90)  # safer than plt.xticks

    plt.tight_layout()
    plt.savefig(savefile)
    plt.close()


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
    tick = 60 * 12
    # plot_spectrum(df, tick, data, plot_utc, 1, 0, 62, title, savefile)
    plot_spectrum(df, tick, delta_pressure, data, plot_utc, 1, 5, 80, title, savefile)

