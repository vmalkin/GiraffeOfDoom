from datetime import timezone, datetime
import constants as k
import matplotlib.pyplot as plt
import os
import class_aggregator

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_spectrum(datetimeformat, tickinterval, data, datetimes, plotfrequency, minv, maxv, plottitle, savefile):
    frequency = 1 / plotfrequency
    plt.figure(layout="constrained", figsize=(17, 7))
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

    df = "%d %H:%M"
    title = "Spectrogram of Barometric Pressure"
    savefile = k.dir_images['images'] + os.sep + "spectrum_press.png"
    tick = 60 * 60
    plot_spectrum(df, tick, plot_press, plot_utc, 1, 0, 30, title, savefile)

    # Spectrogram of seismic readings
    print("Seismic Spectrogram")
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
    spectrum_utc = plot_utc
    spectrum_seismo = plot_seismo
    df = "%d %H:%M"
    title = "Spectrogram of Tilt Readings"
    savefile = k.dir_images['images'] + os.sep + "spectrum_seismo.png"
    tick = 60 * 10 * 60
    plot_spectrum(df, tick, spectrum_seismo, spectrum_utc, 1, -10, 20, title, savefile)

