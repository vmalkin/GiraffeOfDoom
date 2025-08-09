import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import standard_stuff
# import os

ink_colour = "#7a3f16"
def plot_time_data(utcdates, pressuredata, readings_per_tick, texttitle, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)

    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    ax.plot(utcdates, pressuredata, c=ink_colour, linewidth=1)

    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.set_ylim([300, 600])
    # ax.set_xlim([0, 0.3])
    plt.xticks(rotation=90)

    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M.%f')
    plot_title = texttitle + " (Arbitrary Units) - " + ut

    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)


def plot_spectrum(data, savefile):
    frequency = 1 / 5
    # d = []
    # t = []
    # #
    # # for item in data:
    # #     d.append(item[1])
    # #     t.append(item[0])

    plt.figure(figsize=(15, 5))
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=128, noverlap=32, detrend='mean', Fs=frequency, cmap='inferno', vmin=0, vmax=50)

    # print("Pxx shape:", Pxx.shape)
    # print("Frequency bins:", freqs.shape)
    # print("Time bins:", bins.shape)
    # print("Pxx min/max:", Pxx.min(), "/", Pxx.max())
    # print("Pxx sample (dB):", 10 * np.log10(Pxx[0:3, 0:5]))  # Convert to dB to match what you see in the image

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title('Spectrogram')

    savefile = savefile
    plt.savefig(savefile)
    plt.close()