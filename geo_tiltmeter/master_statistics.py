from scipy.stats import pearsonr
from scipy.signal import welch, butter, sosfiltfilt
import standard_stuff
import time
import class_aggregator
import os
import constants as k
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import colors as mcolors
import matplotlib.dates as mdates

def colour_list(size):
    returnlist = []
    # c = ['#c7a5aa', '#b19297', '#9c8185', '#877074', '#735e62', '#5e4d50', '#4a3c3f', '#352b2d', '#21191c', '#0c080a']
    c = ['#00202e', '#2c4875', '#8a508f', '#bc5090', '#ff6361', '#ff8531', '#ffa600', '#80d353', '#609f3f', '#406a2a']
    for i in range(0, size):
        j = int((i / size) * 10)
        returnlist.append(c[j])
    return returnlist


def marker_list(size):
    returnlist = []
    m = ["$0$","$1$","$2$","$3$","$4$","$5$","$6$","$7$", "$8$","$9$"]
    for i in range(0, size):
        j = int((i / size) * 10)
        returnlist.append(m[j])
    return returnlist


def plot_scatter(x_data, y_data, filename, title):
    result = pearsonr(x_data, y_data)
    pearson_corr = round(result[0], 2)
    fig, ax = plt.subplots(nrows=2, height_ratios=[10, 1], figsize=(10, 11))
    colours = colour_list(len(x_data))
    markers = marker_list(len(x_data))
    ax[0].scatter(x_data, y_data, c=colours, marker='o', s=20, linewidth=1, alpha=0.7)
    ax[0].set_title(title)
    # plt.xlabel("UTC Datetime.")
    for i in range(0, len(colours)):
        ax[1].scatter(i, 1, c=colours[i], marker='o', s=20, linewidth=1, alpha=0.7)
    ax[1].set_xlabel(f"<-- Older Data       pearson_r={pearson_corr}       Newer Data -->")
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    savefile = k.dir_saves['images'] + os.sep + filename + '.png'
    plt.savefig(savefile)
    plt.close()


def plot(spectrum_subarrays, dateformat, filename, plottitle):
    plotstyle = 'Solarize_Light2'
    plt.style.use(plotstyle)
    plotrows = len(spectrum_subarrays) - 1

    # fig, ax = plt.subplots(plotrows, layout="constrained", height_ratios=[1,1,1], figsize=(16, 32), dpi=250)
    fig, ax = plt.subplots(plotrows, layout="constrained", figsize=(16, 32), dpi=250, sharex=True)

    my_fmt = mdates.DateFormatter(dateformat)
    for i in range(1, len(spectrum_subarrays)):
        utcdateobjects = spectrum_subarrays[0][2]
        data = spectrum_subarrays[i][2]
        ylabel = spectrum_subarrays[i][0]
        xlabel = spectrum_subarrays[i][1]
        ax[i - 1].plot(utcdateobjects, data, c='black', linewidth=1)
        ax[i - 1].grid(which='major', linestyle=':', color='white', alpha=1)
        ax[i - 1].grid(which='minor', linestyle=':', color='white',alpha=0.5)
        # Minor ticks and grid
        ax[i - 1].xaxis.set_minor_locator(AutoMinorLocator(6))
        ax[i - 1].yaxis.set_minor_locator(AutoMinorLocator(1))
        ax[i - 1].xaxis.set_major_formatter(my_fmt)
        ax[i - 1].set_ylabel(ylabel)
        ax[i - 1].set_xlabel(xlabel)

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
    ax[0].set_title(plottitle)
    # plt.xlabel("UTC Datetime.")
    savefile = k.dir_saves['images'] + os.sep + filename + '.png'
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

    # We want to use low-frequency data under the assumption that above about 1hz, most of the noise is manmade.
    sanitised_list = np.array(sanitised_list)
    posix_data = sanitised_list[:, 0]
    seis_data = sanitised_list[:, 1]
    temp_data = sanitised_list[:, 2]
    pressure_data = sanitised_list[:, 3]

    # use a 4-pole butterworth filter to get low frequency seismic signals
    lowvalue = 0.0001
    highvalue = 0.3
    sos = butter(
        4,
        [lowvalue, highvalue],
        btype='bandpass',
        fs=k.datapersecond,
        output='sos'
    )
    filtered_data = sosfiltfilt(sos, seis_data)

    # CREATE aggregated data
    # [utc_object_time, seismic_data, temperature_data, pressure_data]
    print(f'*** BEGIN Plotter ***\n')

    start = time.time()

    # window of 10 minutes
    halfwindow = 5 * 60 * k.datapersecond
    # in 5 minutes steps
    step = 5 * 60 * k.datapersecond

    aggregate_array = []
    for i in range(halfwindow, len(filtered_data) - halfwindow, step):
        date_start = posix_data[i - halfwindow]
        date_end = posix_data[i + halfwindow]
        d = class_aggregator.Aggregator(date_start, date_end)
        d.data_seismo = filtered_data[i - halfwindow: i + halfwindow + 1]
        d.data_pressure = pressure_data[i - halfwindow: i + halfwindow + 1]
        d.data_temperature = temp_data[i - halfwindow: i + halfwindow + 1]
        aggregate_array.append(d)

    # We now have an array of data objects with our total data windowed at set intervals.

    df = "%b %d \n%Hhr"
    title = f'Stats. Halfwindow of {halfwindow} samples every {step} samples.'
    plot(spectrumdata_7, df, 'stats_seven_day', title)
    plot(spectrumdata_1, df, 'stats_one_day', title)

    #
    # # Scatterplots
    # plot_scatter(stddev_data, skews_data, filename='sctr_7_sd_skw', title='x: SD, y: Skew')
    # plot_scatter(temperature_data, seismic_data, filename='sctr_7_tlt_temp', title='x: Temp, y: Tilt')
    # plot_scatter(temperature_data, pressure_data, filename='sctr_7_tmp_prs', title='x: Temp, y: Pressure')
    # plot_scatter(spectral_entropy_data, stddev_data, filename='sctr_7_ent_std', title='x: Spectral Entropy, y: StdDev')
    # plot_scatter(spectral_entropy_data, skews_data, filename='sctr_7_ent_skw', title='x: Spectral Entropy, y: Skew')
    #
    #

    # # =========================================================
    # # Some stats on processing time.
    # end = time.time()
    # elapsed_time = end - start
    # print(f"\n")
    # print(f"Elapsed time: {elapsed_time / 60:.2f} minutes.")
    # print(f'\n*** END Plotter ***')