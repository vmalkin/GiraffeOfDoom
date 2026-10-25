# This template uses multiprocessing to iterate over very large arrays of data. We will use the
# ProcessPoolExecutor as it's considered the more modern method.
# Yes - AI has helped me with the ideas, but as you can tell by the janky code, that bit is mine.

from concurrent.futures import ProcessPoolExecutor
import class_aggregator
import standard_stuff
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
import time
import os
import constants as k
import numpy as np

# There may be other functions here called by process_chunk
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


def process_chunk(chunk):
    # This is a _Worker_ which typically uses the chunk to process then generate a
    # single plot from this chunk. Return the filename of the plot.
    # Data is in form [posix, data1, data2, etc]. use aggregator to separate out.
    if chunk is not None:
        fftdata = class_aggregator.aggregate_data(windowsize=1, querydata=chunk)
        utctimes = fftdata[0]
        data = fftdata[1]
        df = "%d  %H:%M"
        begintime = utctimes[0].strftime(df)
        endtime = utctimes[len(utctimes) - 1].strftime(df)
        day_file_name = utctimes[len(utctimes) - 1].strftime('%Y-%m-%d-%H-%M')
        fft_data = perform_fft(data, k.datapersecond)
        title = f"FFT for time {begintime} to {endtime}. Sample length {len(data)}."
        plot_sevenday_fft(fft_data, begintime, endtime, day_file_name, title)
        return day_file_name


def chunks(data, chunkstep, chunklength):
    # In Python, yield turns a normal function into a generator so
    # it can produce values one at a time instead of returning everything at once.
    # Each time the generator runs up to a yield, it pauses and gives the value to
    # the caller, then continues later from where it left off. THis memory efficient
    for i in range(len(data), 0, -1 * chunkstep):
        if i - chunklength > 0:
            slicestart = i - chunklength
            sliceend = i
            seismo_data = data[slicestart:sliceend]
            yield seismo_data
        else:
            yield None


def main():
    # each entry in data is [posix, data1, data2, etc].
    # The size of the FFT data we want to process (6 hours)
    print(f'*** BEGIN load CSV data ***')
    # Decide on time interval we are plotting for. We can split off smaller intervals based on a larger list
    # Parse logfile directory for file names that fit our interval
    # The Master List is no more than the last 7 days of data.
    duration_seconds = 86400 * 7
    end_time = int(time.time())
    endfile = standard_stuff.posix2utc(end_time, '%Y-%m-%d') + '.csv'
    start_time = int(end_time - duration_seconds)
    startfile = standard_stuff.posix2utc(start_time, '%Y-%m-%d') + '.csv'

    # Get the list of logfiles
    logfile_list = os.listdir(k.dir_saves['logs'])
    logfile_list.sort()

    # Item is the filename. We can just use comparisons to identify files that are alphabetically in range
    # Those that are will have their data appended to a master list.
    masterlist = []
    for item in logfile_list:
        if item >= startfile:
            # "item <= endfile" will include the current UTC day's data.
            if item <= endfile:
                # to load the file, dont forget to prepend the path to the file!
                logfile = k.dir_saves['logs'] + os.sep + item
                with open(logfile, 'r') as f:
                    for line in f:
                        # remove the carriage return
                        line = line.strip()
                        line = line.split(',')
                        l = [float(line[0]), float(line[1]), float(line[2]), float(line[3])]
                        masterlist.append(l)

    # We now have a master list of all data! Sort into order by posix time.
    masterlist.sort(key=lambda item: item[0])
    print(f'*** END load CSV data ***\n')

    # We do need to sanitise the master list. Nans must be deleted from seismic data
    sanitised_list = []
    for item in masterlist:
        if np.isnan(item[1]):
            print(f'{item} is purged.')
        else:
            sanitised_list.append(item)
    # CREATE aggregated data
    # [utc_object_time, seismic_data, temperature_data, pressure_data]
    print(f'*** BEGIN Plotter ***\n')
    two_day_slice_interval = -1 * (86400 * k.datapersecond) * 2
    two_day_slice = sanitised_list[two_day_slice_interval:]

    chunklength = (k.datapersecond * 60) * 60 * 6
    # The next step we're picking the data off from. (Every 5 mins usually)
    chunkstep = (k.datapersecond * 60) * 5
    cores = 3

    # while chunks(data, chunkstep, chunklength) is not None:
    #     d = chunks(data, chunkstep, chunklength)
    #     for item in d:
    #         if item is not None:
    #             print(len(item))
    with ProcessPoolExecutor(max_workers=cores) as executor:
        results = list(
            executor.map(
                process_chunk,
                chunks(two_day_slice, chunkstep, chunklength)
                )
            )
        return results

if __name__ == '__main__':
    main()