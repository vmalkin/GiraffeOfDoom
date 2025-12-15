from datetime import timezone, datetime
import constants as k
import matplotlib.pyplot as plt
import os
import class_aggregator
# from scipy.signal import butter, filtfilt
from scipy.signal import detrend

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_spectrum(datetimeformat, tickinterval, data, datetimes, plotfrequency, minv, maxv, plottitle, savefile):
    nfft = 2048
    noverlap = int(nfft * 0.75)
    plt.figure(layout="constrained", figsize=(17, 7))
    plt.style.use(plotstyle)
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency, cmap='inferno', vmin=minv, vmax=maxv)
    # Pxx, freqs, bins, im = plt.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency,
    #                                     cmap='inferno')
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

    seis_pos_x = 0
    seis_pos_y = 10 ** -1
    plt.annotate("~10 sec period", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
                 bbox=dict(boxstyle="round", fc="1", color='black'))

    seis_pos_x = 0
    seis_pos_y = 10 ** -3
    plt.annotate("~15–20 min period\nLocal turbulence. ", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
                 bbox=dict(boxstyle="round", fc="1", color='black'))

    seis_pos_x = 0
    seis_pos_y = 10 ** -2.5
    plt.annotate("~2–15 min period\nPassing gust fronts, convection boundaries.", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
                 bbox=dict(boxstyle="round", fc="1", color='black'))
    seis_pos_x = 0
    seis_pos_y = 10 ** -4
    plt.annotate("~2–3 hr period\nSlow weather evolution", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=8, color='black',
                 bbox=dict(boxstyle="round", fc="1", color='black'))

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.yscale('log')
    plt.ylim(10**-4.2, 0.5)
    plt.title(plottitle)


    savefile = savefile
    plt.savefig(savefile)
    plt.close()


def wrapper(data):
    print("Barometric Spectrogram - Past 24 hours")
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

    # b, a = butter(2, 0.001, btype='highpass', fs=1)
    # data = filtfilt(b, a, plot_press)
    data = detrend(plot_press, type='linear')

    df = "%d %H:%M"
    title = "*** Spectrogram of Barometric Pressure"
    savefile = k.dir_images['images'] + os.sep + "spectrum_press.png"
    tick = 60 * 60 * 1
    plot_spectrum(df, tick, data, plot_utc, 1, 0, 60, title, savefile)

