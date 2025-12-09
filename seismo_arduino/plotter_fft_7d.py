import numpy as np
from scipy.fft import rfft, rfftfreq
import constants as k
import matplotlib.pyplot as plt
import os
import constants as k


def make_decimal(string_value):
    result = 0
    try:
        result = float(string_value)
        result = round(result, 4)
    except ValueError:
        print("ERROR - string is not a number.")
    return result


def perform_fft(item, seconds_per_data):
    sample_freq = 1 / seconds_per_data
    try:
        yf = rfft(item)
        yf = np.abs(yf)
        xf = rfftfreq(len(item), 1 / sample_freq)
        dp = [xf, yf]
        return dp
    except:
        return ("error_fft")


def plot_sevenday_fft(fft_data):
    # fft data is [xf, yf]
    xf = fft_data[0]
    x_scale_title = "Period - Hz"
    yf = fft_data[1]
    plt.figure(layout="constrained", figsize=(17, 7))
    plt.style.use('Solarize_Light2')
    plt.plot(xf, yf, linewidth=1)
    plt.xlabel(x_scale_title)

    an_pos_y = 10 ** 3.1

    ann_pos_x = 10 ** -1
    plt.annotate("10 s", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -1.7785
    plt.annotate("60 s", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -2.7785
    plt.annotate("10 m", xy=(ann_pos_x, an_pos_y),xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red', bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -3.25528
    plt.annotate("30 m", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -3.5564
    plt.annotate("1 hr", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -4.3347
    plt.annotate("6 hrs", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -4.6355
    plt.annotate("12 hrs", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 **-4.9366
    plt.annotate("1 day", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 **-5.2376
    plt.annotate("2 days", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    plt.ylim(10**2, 10**7)
    # ax.set_xlim([0, 0.3])
    plt.yscale("log")
    plt.xscale("log")
    plt.title("7 Day FFT")
    plt.grid(color='white', linestyle='-', linewidth='2')
    savefile = k.dir_images['images'] + os.sep + "fft.png"
    plt.savefig(savefile)
    plt.close()


def wrapper(csvdata):
    print(f'*** Creating FFT.')
    data = []
    for i in range(0, len(csvdata)):
        data_info = csvdata[i][1]
        decimal_data = make_decimal(data_info)
        data.append(decimal_data)

    fft_data = perform_fft(data, k.sensor_reading_frequency)
    plot_sevenday_fft(fft_data)

