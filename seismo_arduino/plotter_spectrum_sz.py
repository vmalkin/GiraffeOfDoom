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
    nfft = 1024
    noverlap = int(nfft * 0.75)
    plt.figure(layout="constrained", figsize=(17, 7))
    plt.style.use(plotstyle)
    # Pxx, freqs, bins, im = plt.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency, cmap='inferno')
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=nfft, noverlap=noverlap, detrend='mean', Fs=plotfrequency,
                                        cmap='inferno', vmin=minv, vmax=maxv)
    cbar = plt.colorbar(im)
    cbar.set_label('Power / Frequency (dB/Hz)')
    print(f'{len(datetimes)}, {len(data)}')
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
    # Spectrogram of seismic readings
    print("*** Seismic Spectrogram")
    aggregate_array = data
    aggregate_array.pop(0)
    plot_utc = []
    plot_seismo = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i][1]
        plot_utc.append(tim)
        plot_seismo.append(siz)
    spectrum_utc = plot_utc
    spectrum_seismo = plot_seismo
    df = "%d %H:%M"
    title = "Spectrogram of Tilt Readings"
    savefile = k.dir_images['images'] + os.sep + "spectrum_seismo.png"
    tick = 60 * 10 * 60
    plot_spectrum(df, tick, spectrum_seismo, spectrum_utc, 10, -20, 20, title, savefile)

