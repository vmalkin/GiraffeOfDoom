import numpy as np
from scipy.fft import rfft, rfftfreq
from datetime import timezone, datetime
import constants as k
import matplotlib.pyplot as plt
import os
import constants as k
import gc


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


def plot_sevenday_fft(fft_data, begintime, endtime, filename, title):
    # fft data is [xf, yf]
    xf = fft_data[0]
    yf = fft_data[1]
    plt.style.use('Solarize_Light2')

    fig, ax = plt.subplots(2, layout="constrained", height_ratios=[2, 1], figsize=(16, 9), dpi=120)
    ax[0].plot(xf, yf, linewidth=1)
    ax[1].plot(xf, yf, linewidth=1)
    #
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Power (dBm)')
    ax[0].grid(which='major', linestyle='-', linewidth=2, color='white', alpha=1)
    ax[0].grid(which='minor', linestyle='-', linewidth=0.5, color='white', alpha=1)
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Power (dBm)')
    ax[1].grid(which='major', linestyle='-', linewidth=2, color='white', alpha=1)
    ax[1].grid(which='minor', linestyle='-', linewidth=0.5, color='white', alpha=1)
    # Customisation for full FFT
    ax[0].set_ylim(10 ** 0, 10 ** 6)
    ax[0].set_yscale("log")
    ax[0].set_xscale("log")
    # Customisation for Eigenmode frequencies
    ax[1].set_ylim(5 * 10 ** 2, 10 ** 5.1)
    ax[1].set_xlim(10 ** -3, 10 ** -1)
    # ax[1].set_xlim(1.5 * (10 ** -3), 2 * (10 ** -3))
    ax[1].set_yscale("log")
    ax[1].set_xscale("log")

    ax[0].set_title(title)

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
        ax[0].annotate(item[1],
                     xy=(ann_pos_x, an_pos_y),
                     xytext=(ann_pos_x, an_pos_y),
                     fontsize=7,
                     color=item[2],
                     bbox=dict(boxstyle="square", fc="1", color=item[2]))

    interest_labels = [
        [10 ** -1.23044892137827, '1pr uSm', 'green'],
        [10 ** -0.698970004336019, '2nd uSm', 'green'],
        [10 ** -0.204119982655925, 'Pendulum natural period', 'green']
    ]
    an_pos_y = 10 ** 0.7
    for item in interest_labels:
        ann_pos_x = (item[0])
        ax[0].annotate(item[1],
                     xy=(ann_pos_x, an_pos_y),
                     xytext=(ann_pos_x, an_pos_y),
                     fontsize=7,
                     color=item[2],
                     bbox=dict(boxstyle="square", fc="1", color=item[2]))

    earth_normal_modes = [
        [10 ** -3.50933695801764, "0S2"],
        [10 ** -3.42324587393681, "0T2"],
        [10 ** -3.39357520326959, "2S1"],
        [10 ** -3.32919441508845, "0S3"],
        [10 ** -3.23095955574857, "0T3"],
        [10 ** -3.18920948958231, "0S4"],
        [10 ** -3.16761267272753, "1S2"],
        [10 ** -3.1152775913959, "0T4"],
        [10 ** -3.08919836680515, "0S0"],
        [10 ** -3.07554696139253, "0S5"],
        [10 ** -3.03221570329798, "0T5"],
        [10 ** -3.02775720469055, "2S2"],
        [10 ** -3.02694162795903, "1S3"],
        [10 ** -3.02489596010749, "3S1"],
        [10 ** -2.98407703390283, "0S6"],
        [10 ** -2.9670797341445, "0T6"],
        [10 ** -2.95616843047536, "3S2"],
        [10 ** -2.9304395947667, "1S4"],
        [10 ** -2.91328390176042, "0T7"],
        [10 ** -2.90955602924118, "0S7"],
        [10 ** -2.90794852161227, "1T1"],
        [10 ** -2.90525604874845, "2S3"],
        [10 ** -2.87966920563205, "1T2"],
        [10 ** -2.86746748785905, "0T8"],
        [10 ** -2.86332286012046, "1S5"],
        [10 ** -2.86033800657099, "2S4"],
        [10 ** -2.85003325768977, "0S8"],
        [10 ** -2.84198480459011, "1T3"],
        [10 ** -2.82736927305383, "0T9"],
        [10 ** -2.81954393554187, "2S5"],
        [10 ** -2.81756536955978, "1S6"],
        [10 ** -2.80208925788173, "0S9"],
        [10 ** -2.79169064902012, "0T10"],
        [10 ** -2.78746047451842, "1S0"],
        [10 ** -2.78103693862113, "1S7"],
        [10 ** -2.77451696572855, "2S6"],
        [10 ** -2.76342799356294, "0S10"],
        [10 ** -2.74507479158206, "1S8"],
        [10 ** -2.72997428569956, "0S11"],
        [10 ** -2.71516735784846, "1T6"],
        [10 ** -2.70757017609794, "1S9"],
        [10 ** -2.70329137811866, "0T13"],
        [10 ** -2.70156798505593, "0S12"]
    ]
    an_pos_y = 10 ** 5
    for item in earth_normal_modes:
        ann_pos_x = (item[0])
        ax[1].annotate(item[1],
                     xy=(ann_pos_x, an_pos_y),
                     xytext=(ann_pos_x, an_pos_y),
                     fontsize=6,
                     color='blue',
                     bbox=dict(boxstyle="square", fc="1", color="red"))
    savefile = k.dir_saves['spectrograms'] + os.sep + str(filename) + ".png"
    plt.savefig(savefile)
    plt.clf()
    plt.close()


def wrapper(utctime, csvdata, timeslice, datafreq, samplelength):
    # utctime - utc time object array
    # csvdata - data array. Should be same length as utctime
    # timeslice - how many datapoints will be used for each FFT plot
    # datapersecond - how many readings per second. This may be different from the seismo freq
    print(f'*** Creating FFT movie frames')
    # The FFT will be for data this long...
    # at intervals of this
    plot_data = csvdata
    plot_utc = utctime
    df = "%d  %H:%M"

    # We will iterate in chunks from now, back to the start of the array to ensure we always plot a chunk for Now
    timestep = (datafreq * 60) * 5
    garbagecounter = 0
    for i in range(len(plot_data), 0, -1 * timestep):
        if i - timeslice > 0:
            slicestart = i - timeslice
            sliceend = i
            seismo_data = plot_data[slicestart:sliceend]
            chart_times = plot_utc[slicestart:sliceend]
            #
            begintime = chart_times[0].strftime(df)
            endtime = chart_times[len(chart_times) - 1].strftime(df)
            day_file_name = chart_times[len(chart_times) - 1].strftime('%Y-%m-%d-%H-%M')
            fft_data = perform_fft(seismo_data, datafreq)
            title = f"FFT for time {begintime} to {endtime}. Sample length {samplelength}."
            plot_sevenday_fft(fft_data, begintime, endtime, day_file_name, title)
            print(f'FFT for time {i}')
            garbagecounter+=1
            if garbagecounter == 20:
                print(f'Perform garbage collection')
                gc.collect()
                garbagecounter = 0
