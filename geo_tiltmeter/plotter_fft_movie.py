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


def perform_fft(item, datapersecond):
    sample_freq = 1 / datapersecond
    try:
        yf = rfft(item)
        yf = np.abs(yf)
        xf = rfftfreq(len(item), sample_freq)
        dp = [xf, yf]
        return dp
    except:
        return ("error_fft")


def plot_sevenday_fft(fft_data, begintime, endtime, filename):
    # fft data is [xf, yf]
    xf = fft_data[0]
    yf = fft_data[1]
    plt.style.use('Solarize_Light2')

    fig, ax = plt.subplots(1, layout="constrained", figsize=(16, 9), dpi=120)
    ax.plot(xf, yf, linewidth=1)
    ax.set_xlabel("Tiltmeter. Arbitrary Units.")

    # label calculated as follows:
    # take period in seconds.
    # Find reciprocal.
    # exponent is log(base 10)
    period_labels = [
        [10 ** 0, '1 sec', 'red'],
        [10 ** -0.301029995663981, '2 sec', 'red'],
        [10 ** -0.698970004336019, '5 sec', 'red'],
        [10 ** -1, '10 sec', 'red'],
        [10 ** -1.30102999566398, '20 sec', 'red'],
        [10 ** -1.47712125471966, '30 sec', 'red'],
        [10 ** -1.77815125038364, '1 min', 'red'],
        [10 ** -2.07918124604762, '2 min', 'red'],
        [10 ** -2.47712125471966, '5 min', 'red'],
        [10 ** -2.77815125038364, '10 min', 'red'],
        [10 ** -3.25527250510331, '30 min', 'red'],
        [10 ** -3.55630250076729, '1 hr', 'red'],
        [10 ** -3.85733249643127, '2 hr', 'red'],
        [10 ** -4.33445375115093, '6 hr', 'red'],
        [10 ** -4.63548374681491, '12 hr', 'red']
    ]
    an_pos_y = 10 ** 1
    for item in period_labels:
        ann_pos_x = (item[0])
        ax.annotate(item[1],
                     xy=(ann_pos_x, an_pos_y),
                     xytext=(ann_pos_x, an_pos_y),
                     fontsize=7,
                     color=item[2],
                     bbox=dict(boxstyle="square", fc="1", color=item[2]))

    interest_labels = [
        [10 ** -1.23044892137827, '1pr uSm', 'green'],
        [10 ** -0.698970004336019, '2nd uSm', 'green'],
        [10 ** -0.25, 'Pendulum natural period', 'green']
    ]
    an_pos_y = 10 ** 0.7
    for item in interest_labels:
        ann_pos_x = (item[0])
        ax.annotate(item[1],
                     xy=(ann_pos_x, an_pos_y),
                     xytext=(ann_pos_x, an_pos_y),
                     fontsize=7,
                     color=item[2],
                     bbox=dict(boxstyle="square", fc="1", color=item[2]))

    ax.set_ylim(10 ** 0, 10 ** 6)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_title("FFT for time" + " - " + begintime + " - " + endtime)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (dBm)')
    ax.grid(which='major', linestyle='-', linewidth=2, color='white', alpha=1)
    ax.grid(which='minor', linestyle='-', linewidth=0.5, color='white', alpha=1)
    savefile = k.dir_saves['spectrograms'] + os.sep + str(filename) + ".png"
    plt.savefig(savefile)
    plt.close()


def wrapper(utctime, csvdata):
    print(f'*** Creating FFT movie frames')
    # The FFT will be for data this long...
    timeslice = (k.datapersecond * 60) * 60
    # at intervals of this
    timestep = (k.datapersecond * 60) * 5
    plot_data = csvdata
    plot_utc = utctime
    df = "%d  %H:%M"

    for i in range(0, len(plot_data), timestep):
        print(f'FFT Frames {i} / {len(plot_data)}')
        array_start = i
        array_end = i + timeslice
        seismo_data = plot_data[array_start:array_end]
        chart_times = plot_utc[array_start:array_end]

        if len(seismo_data) == timeslice:
            begintime = chart_times[0].strftime(df)
            endtime = chart_times[len(chart_times) - 1].strftime(df)
            day_file_name = chart_times[len(chart_times) - 1].strftime('%Y-%m-%d-%H-%M')
            fft_data = perform_fft(seismo_data, k.datapersecond)
            plot_sevenday_fft(fft_data, begintime, endtime, day_file_name)
