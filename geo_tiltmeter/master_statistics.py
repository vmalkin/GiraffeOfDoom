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

plotstyle = 'Solarize_Light2'
df = "%b %d \n%Hhr"

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
    plt.style.use(plotstyle)
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


def plot_sta(stadata, staposix, dateformat):
    plt.style.use(plotstyle)
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 4), dpi=250)
    my_fmt = mdates.DateFormatter(dateformat)
    ax.plot(staposix, stadata, c='black', linewidth=1)
    ax.grid(which='major', linestyle=':', color='white', alpha=1)
    ax.grid(which='minor', linestyle=':', color='white', alpha=0.5)
    # Minor ticks and grid
    ax.xaxis.set_minor_locator(AutoMinorLocator(6))
    ax.yaxis.set_minor_locator(AutoMinorLocator(1))
    ax.xaxis.set_major_formatter(my_fmt)
    savefile = k.dir_saves['images'] + os.sep + 'stalta.png'
    plt.savefig(savefile)
    plt.close()


def plot(spectrum_subarrays, ylabels, dateformat, filename, plottitle):
    plt.style.use(plotstyle)
    plotrows = len(spectrum_subarrays) - 1
    # fig, ax = plt.subplots(plotrows, layout="constrained", height_ratios=[1,1,1], figsize=(16, 32), dpi=250)
    fig, ax = plt.subplots(plotrows, layout="constrained", figsize=(16, 32), dpi=250, sharex=False)

    my_fmt = mdates.DateFormatter(dateformat)
    for i in range(1, len(spectrum_subarrays)):
        utcdateobjects = spectrum_subarrays[0]
        data = spectrum_subarrays[i]
        y_label = ylabels[i]
        # xlabel = spectrum_subarrays[i][1]
        ax[i - 1].plot(utcdateobjects, data, c='black', linewidth=1)
        ax[i - 1].grid(which='major', linestyle=':', color='white', alpha=1)
        ax[i - 1].grid(which='minor', linestyle=':', color='white',alpha=0.5)
        # Minor ticks and grid
        ax[i - 1].xaxis.set_minor_locator(AutoMinorLocator(6))
        ax[i - 1].yaxis.set_minor_locator(AutoMinorLocator(1))
        ax[i - 1].xaxis.set_major_formatter(my_fmt)
        ax[i - 1].set_ylabel(y_label)
        # ax[i - 1].set_xlabel(xlabel)

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
    # demean the seismic data
    seis_data = seis_data - np.mean(seis_data)

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
    # The butterworth filter DOES have an end-effect. We are going to trim this and shorted all other data
    # so it's the same length
    trimvalue = 4 * 60 * 60 * k.datapersecond
    filtered_data = filtered_data[trimvalue:-trimvalue]
    posix_data = posix_data[trimvalue:-trimvalue]
    temp_data = temp_data[trimvalue:-trimvalue]
    pressure_data = pressure_data[trimvalue:-trimvalue]
    print(f'{len(filtered_data)}')

    # # Create the sta/lta plot at this point
    # stalta = []
    # halfw_sta = 30 * k.datapersecond
    # halfw_lta = 3 * 60 * k.datapersecond
    # for i in range(halfw_lta, len(filtered_data) - halfw_lta):
    #     sta = filtered_data[i-halfw_sta:-i+halfw_sta]
    #     lta = filtered_data[i-halfw_lta:-i+halfw_lta]
    #     d = np.mean(sta) / np.mean(lta)
    #     stalta.append(d)
    # psxtemp = posix_data[halfw_lta:-halfw_lta]
    # stapsx = []
    # for item in psxtemp:
    #     utcobj = item.return_utc_timeobject(item)
    #     stapsx.append(utcobj)
    # plot_sta(stalta, stapsx, df)

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
    # Let's extract plottable data

    utcobjects = []
    for item in aggregate_array:
        utc = item.get_avg_posix()
        utcobj = item.return_utc_timeobject(utc)
        utcobjects.append(utcobj)

    data_mean = []
    for item in aggregate_array:
        dmn = item.get_data_avg(item.data_seismo)
        data_mean.append(dmn)

    data_skw_p = []
    for item in aggregate_array:
        d = item.get_skew_parsons(item.data_seismo)
        data_skw_p.append(d)

    data_skw_3rd = []
    for item in aggregate_array:
        d = item.get_skew_3rdCM(item.data_seismo)
        data_skw_3rd.append(d)

    data_stdev = []
    for item in aggregate_array:
        d = item.get_stddev(item.data_seismo)
        data_stdev.append(d)

    spectral_entropy = []
    for item in aggregate_array:
        d = item.get_spectral_entropy(item.data_seismo)
        spectral_entropy.append(d)

    temp = []
    for item in aggregate_array:
        d = item.get_data_avg(item.data_temperature)
        temp.append(d)

    press = []
    for item in aggregate_array:
        d = item.get_data_avg(item.data_pressure)
        press.append(d)

    spectrumdata = [
        utcobjects,
        data_mean,
        temp,
        press,
        data_skw_p,
        data_stdev,
        spectral_entropy
    ]

    ylabels = [
        '',
        'Mean of tilt data.',
        'Room temperature',
        'Room pressure.',
        'Pearsons Skew',
        'Standard Deviation',
        'Spectral Entropy'
    ]

    title = f'Stats. Window of {2 * halfwindow} samples every {step} samples. {lowvalue}hz to {highvalue}hz.'
    plot(spectrumdata, ylabels, df, 'stats_seven_day', title)
    # # plot(spectrumdata_1, df, 'stats_one_day', title)
    #
    # #
    # # # Scatterplots
    plot_scatter(data_skw_p, data_skw_3rd, filename='sctr_7_skw_skw', title='x: skw-p, y: skw-3')
    plot_scatter(temp, data_mean, filename='sctr_7_tlt_temp', title='x: Temp, y: Tilt')
    # # plot_scatter(temperature_data, pressure_data, filename='sctr_7_tmp_prs', title='x: Temp, y: Pressure')
    # # plot_scatter(spectral_entropy_data, stddev_data, filename='sctr_7_ent_std', title='x: Spectral Entropy, y: StdDev')
    # # plot_scatter(spectral_entropy_data, skews_data, filename='sctr_7_ent_skw', title='x: Spectral Entropy, y: Skew')
    # #
    # #
    #
    # # # =========================================================
    # # # Some stats on processing time.
    # # end = time.time()
    # # elapsed_time = end - start
    # # print(f"\n")
    # # print(f"Elapsed time: {elapsed_time / 60:.2f} minutes.")
    # # print(f'\n*** END Plotter ***')