import os
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import standard_stuff
import os

ink_colour = "#7a3f16"
def plot_time_data(utcdates, pressuredata, readings_per_tick, texttitle, savefile):
    # ('constellation', 'satID', posixtime, alt, azi, snr)

    plt.style.use('Solarize_Light2')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
    ax.plot(utcdates, pressuredata, c=ink_colour, linewidth=1)

    tick_spacing = readings_per_tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # ax.set_ylim([400, 500])
    # ax.set_xlim([0, 0.3])
    plt.xticks(rotation=90)

    pt = time.time()
    ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M.%f')
    plot_title = texttitle + " (Arbitrary Units) - " + ut

    ax.set_title(plot_title)
    # plt.show()
    plt.savefig(savefile)
    plt.close()


def plot_hourly_array(utcdates, sensor_data, save_path):
    # Data is about 5 readings per second. Calculate how many readings for an hour
    window = 5 * 60 * 120
    index_start = 0
    index_end = window

    for i in range(0, 50):
        hour_data = sensor_data[index_start: index_end]
        hour_utc = utcdates[index_start: index_end]

        try:
            plt.style.use('Solarize_Light2')
            fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
            ax.plot(hour_utc, hour_data, c=ink_colour, linewidth=1)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(3000))
            ax.set_ylim([400, 500])
            # ax.set_xlim([0, 0.3])
            plt.xticks(rotation=90)

            pt = time.time()
            ut = standard_stuff.posix2utc(pt, '%Y-%m-%d %H:%M.%f')
            texttitle = hour_data[0]
            plot_title = str(texttitle) + " (Arbitrary Units) - " + ut
            savefile = save_path + os.sep + f"{i:03}" + ".png"
            ax.set_title(plot_title)
            plt.savefig(savefile)
            # increment the indices for slicing the array
            index_start = index_end
            index_end = index_end + window
            plt.close()
        except:
            print("Finished")


def plot_spectrum(data, datetimes, plotfrequency, savefile):
    frequency = plotfrequency

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
    #
    # ticks = []
    # for i in range(0, len(datetimes)):
    #     ticks.append(i)
    # plt.xticks(ticks, datetimes)
    savefile = savefile
    plt.savefig(savefile)
    plt.close()