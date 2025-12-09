import numpy as np
from scipy.fft import rfft, rfftfreq
from datetime import timezone, datetime
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


def plot_sevenday_fft(fft_data, begintime, endtime, filename):
    # fft data is [xf, yf]
    xf = fft_data[0]
    x_scale_title = "Period - Hz"
    yf = fft_data[1]
    plt.figure(layout="constrained", figsize=(17, 7))
    plt.style.use('Solarize_Light2')
    plt.plot(xf, yf, linewidth=1)
    plt.xlabel(x_scale_title)

    an_pos_y = 10 ** 3.1

    seis_pos_x = 10 ** -3.7
    seis_pos_y = 10 ** 3.9
    plt.annotate("Earthquake Threshold", xy=(seis_pos_x, seis_pos_y), xytext=(seis_pos_x, seis_pos_y), fontsize=10, color='green',
                 bbox=dict(boxstyle="round", fc="1", color='green'))

    ann_pos_x = 10 ** 0.7
    plt.annotate("0.4 s", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** 0
    plt.annotate("1 s", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -1
    plt.annotate("10 s", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -1.7785
    plt.annotate("60 s", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -2.7785
    plt.annotate("10 m", xy=(ann_pos_x, an_pos_y),xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red', bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -3.25528
    plt.annotate("30 m", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -3.5564
    plt.annotate("1 hr", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -4.3347
    plt.annotate("6 hrs", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 ** -4.6355
    plt.annotate("12 hrs", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 **-4.9366
    plt.annotate("1 day", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos_x = 10 **-5.2376
    plt.annotate("2 days", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10 , color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    plt.ylim(10**1, 10**5)
    # ax.set_xlim([0, 0.3])
    plt.yscale("log")
    plt.xscale("log")
    title = "FFT per hour" + " - " + begintime + " - " + endtime
    plt.title(title)
    plt.grid(color='white', linestyle='-', linewidth='2')
    savefile = k.dir_images['spectrograms'] + os.sep + str(filename) + ".png"
    plt.savefig(savefile)
    plt.close()


def wrapper(csvdata):
    print(f'*** Creating FFT movie frames')
    # The FFT will be for one hour of data...
    timeslice = 10 * 60 * 60
    # IN steps of 10 minutes
    timestep = 10 * 60 * 5
    plot_data = []
    plot_utc = []
    df = "%d  %H:%M"
    for i in range(0, len(csvdata)):
        tim = csvdata[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        data_info = csvdata[i][1]
        decimal_data = make_decimal(data_info)
        plot_data.append(decimal_data)
        plot_utc.append(tim)

    for i in range(0, len(plot_data), timestep):
        array_start = i
        array_end = i + timeslice
        seismo_data = plot_data[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]
        begintime = chart_times[0].strftime(df)
        endtime = chart_times[len(chart_times) - 1].strftime(df)
        fft_data = perform_fft(seismo_data, k.sensor_reading_frequency)
        plot_sevenday_fft(fft_data, begintime, endtime, i)

