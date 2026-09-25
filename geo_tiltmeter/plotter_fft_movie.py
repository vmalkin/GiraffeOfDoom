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

    # label calculated as follows:
    # take period in seconds.
    # Find reciprocal.
    # exponent is log(base 10)
    period_labels = [
        [0, '1 sec', 'red'],
        [-0.301029995663981, '2 sec', 'red'],
        [-0.698970004336019, '5 sec', 'red'],
        [-0.845098040014257, 'Sec uSm', 'green'],
        [-1, '10 sec', 'red'],
        [-1.17609125905568, 'Pr uSm', 'green'],
        [-1.30102999566398, '20 sec', 'red'],
        [-1.47712125471966, '30 sec', 'red'],
        [-1.77815125038364, '1 min', 'red'],
        [-2.47712125471966, '5 min', 'red'],
        [-2.77815125038364, '10 min', 'red'],
        [-3.25527250510331, '30 min', 'red'],
        [-3.55630250076729, '1 hr', 'red'],
        [-3.85733249643127, '2 hr', 'red'],
        [-4.33445375115093, '6 hr', 'red'],
        [-4.63548374681491, '12 hr', 'red']
    ]

    an_pos_y = 10 ** -0.4
    for item in period_labels:
        ann_pos_x = 10 ** (item[0])
        plt.annotate(item[1],
                     xy=(ann_pos_x, an_pos_y),
                     xytext=(ann_pos_x, an_pos_y),
                     fontsize=7,
                     color=item[2],
                     bbox=dict(boxstyle="square", fc="1", color=item[2]))

    # ann_pos_x = 10 **-4.9366
    # plt.annotate("1 day", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10, color='red',
    #              bbox=dict(boxstyle="round", fc="1", color='red'))
    #
    # ann_pos_x = 10 **-5.2376
    # plt.annotate("2 days", xy=(ann_pos_x, an_pos_y), xytext=(ann_pos_x, an_pos_y), fontsize=10 , color='red',
    #              bbox=dict(boxstyle="round", fc="1", color='red'))

    # plt.ylim(10**1, 10**5)
    plt.ylim(10 ** -1, 10 ** 4)
    # ax.set_xlim([0, 0.3])
    plt.yscale("log")
    plt.xscale("log")
    title = "FFT for time" + " - " + begintime + " - " + endtime
    plt.title(title)
    plt.grid(color='white', linestyle='-', linewidth='2')
    savefile = k.dir_saves['spectrograms'] + os.sep + str(filename) + ".png"
    plt.savefig(savefile)
    plt.close()


def wrapper(utctime, csvdata):
    print(f'*** Creating FFT movie frames')
    # The FFT will be for data this long...
    timeslice = k.sensor_reading_frequency * 60 * 60 * 1
    # IN steps of this
    timestep = k.sensor_reading_frequency * 60 * 15
    plot_data = csvdata
    plot_utc = utctime
    df = "%d  %H:%M"

    # if len(csvdata) >= timeslice:
    #     for i in range(0, len(csvdata)):
    #         try:
    #             j = float(csvdata[i])
    #             plot_data.append(j)
    #         except TypeError:
    #             utctime.pop(i)
    #             print(csvdata[i])
        #
        # for i in range(0, len(d)):
        #     data_info = d[i]
        #     decimal_data = make_decimal(data_info)
        #     plot_data.append(decimal_data)
    for i in range(0, len(plot_data), timestep):
        array_start = i
        array_end = i + timeslice
        seismo_data = plot_data[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]

        if len(seismo_data) == timeslice:
            begintime = chart_times[0].strftime(df)
            endtime = chart_times[len(chart_times) - 1].strftime(df)
            day_file_name = chart_times[len(chart_times) - 1].strftime('%Y-%m-%d-%H-%M')
            fft_data = perform_fft(seismo_data, k.sensor_reading_frequency)
            plot_sevenday_fft(fft_data, begintime, endtime, day_file_name)


