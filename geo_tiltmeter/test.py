import standard_stuff
import time
import class_aggregator
import os
import constants as k
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates


def plot(spectrum_subarrays, dateformat):
    plotstyle = 'Solarize_Light2'
    plt.style.use(plotstyle)
    plotrows = len(spectrum_subarrays) - 1

    # fig, ax = plt.subplots(plotrows, layout="constrained", height_ratios=[1,1,1], figsize=(16, 32), dpi=250)
    fig, ax = plt.subplots(plotrows, layout="constrained", figsize=(16, 32), dpi=250)

    my_fmt = mdates.DateFormatter(dateformat)
    for i in range(1, len(spectrum_subarrays)):
        utcdateobjects = spectrum_subarrays[0][1]
        data = spectrum_subarrays[i][1]
        label = spectrum_subarrays[i][0]
        ax[i - 1].plot(utcdateobjects, data, c='black', linewidth=1)
        ax[i - 1].grid(which='major', linestyle=':', color='white', alpha=1)
        ax[i - 1].grid(which='minor', linestyle=':', color='white',alpha=0.5)
        # Minor ticks and grid
        ax[i - 1].xaxis.set_minor_locator(AutoMinorLocator(6))
        ax[i - 1].yaxis.set_minor_locator(AutoMinorLocator(1))
        ax[i - 1].xaxis.set_major_formatter(my_fmt)
        ax[i - 1].set_ylabel(label)

    # # Grids and labels
    # for i in range(0, plotrows - 1):
    #     ax[i].axes.xaxis.set_ticklabels([])
    #
    # for i in range(0, plotrows):
    #
    #
    # ax[1].set_ylabel("Min, Max.")
    # ax[2].set_ylabel("Standard Deviation.")
    # # # ax[0].set_ylim([sz_ymin, sz_ymax])
    # plot_title=(f'Tilt Data Rolling Stats. '
    #             f'Running window: {halfwindow * 2} samples@ {k.datapersecond}/sec. '
    #             f'Plotted: {standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')}')
    # ax[0].set_title(plot_title)
    # plt.xlabel("UTC Datetime.")
    savefile = k.dir_saves['images'] + os.sep + 'stats.png'
    plt.savefig(savefile)
    plt.close()


if __name__ == '__main__':
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
    one_day_slice_interval = -1 * (86400 * k.datapersecond) * 7
    one_day_slice = sanitised_list[one_day_slice_interval:]
    start = time.time()

    # window of 10 minutes
    window = 10 * 60 * k.datapersecond
    spectrumdata = class_aggregator.aggregate_data(window, one_day_slice)

    df = "%b %d \n%Hhr"
    plot(spectrumdata, df)

    # =========================================================
    # Some stats on processing time.
    end = time.time()
    elapsed_time = end - start
    print(f"\n")
    print(f"Elapsed time: {elapsed_time / 60:.2f} minutes.")
    print(f'\n*** END Plotter ***')