import mgr_database
import standard_stuff
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np
from scipy.signal import savgol_filter, detrend
import os
import constants as k
import class_aggregator


def plot_autocorrelation(autocdata, tickinterval, plottitle, legend, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(19, 6), dpi=140)
    # plotcolours = ["#003049", "#d62828", "#f77f00"]
    plotcolours = ['#00202e', '#2c4875', '#8a508f', '#bc5090', '#ff6361', '#ff8531', '#ffa600', '#80d353', '#609f3f', '#406a2a']
    for i in range(0, len(autocdata)):
        ax.plot(autocdata[i], c=plotcolours[i], linewidth=1)

    ax.xaxis.set_major_locator(plt.MultipleLocator(tickinterval))
    # ax.set_xlim([0, int(len(autocdata[0] / 2))])
    plt.legend(legend, loc='lower center')
    plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks
    plot_title = plottitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax.set_title(plot_title)
    plt.tight_layout()
    plt.savefig(savefile)
    plt.close()


if __name__ == "__main__":
    print(f'*** BEGIN load CSV data ***')
    # Get the list of logfiles
    logfile_list = os.listdir(k.dir_saves['logs'])
    logfile_list.sort()

    # Item is the filename. We can just use comparisons to identify files that are alphabetically in range
    # Those that are will have their data appended to a master list.
    masterlist = []
    for item in logfile_list:
        # if item >= startfile:
        #     # "item <= endfile" will include the current UTC day's data.
        #     if item <= endfile:
        #         # to load the file, dont forget to prepend the path to the file!
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

    # sanitised_list = np.array(sanitised_list)
    # posix_data = sanitised_list[:, 0]
    # seis_data = sanitised_list[:, 1]
    # temp_data = sanitised_list[:, 2]
    # pressure_data = sanitised_list[:, 3]
    # # detrend the seismic data
    # seis_data = detrend(seis_data, type='linear')

    # decimate to clean bins, no overlap, of 1 minutes
    halfwindow = 30 * k.datapersecond
    step = halfwindow * 2
    spectrumdata = class_aggregator.basic_aggregated_list(sanitised_list,halfwindow, step)
    # utctimes = []
    data = []
    # temperature = []
    # pressure = []
    for item in spectrumdata:
        dd = item.get_data_avg(item.data_seismo)
        # tt = item.get_data_avg(item.data_temperature)
        # pp = item.get_data_avg(item.data_pressure)
        # to = item.return_utc_timeobject(item.get_avg_posix())
        data.append(dd)
        # temperature.append(tt)
        # pressure.append(pp)
        # utctimes.append(to)

    # Compute autocorrelation
    # https://www.scicoding.com/4-ways-of-calculating-autocorrelation-in-python/
    # Mean
    mean = np.mean(data)

    # Variance
    var = np.var(data)

    # Normalized data
    decimated_data = data - mean
    ac = np.correlate(decimated_data, decimated_data, mode='full')[len(decimated_data)-1:]
    ac = ac / var / len(decimated_data)
    autocorr = []
    autocorr.append(ac)

    # Compute residuals using a Savitzky Golay Filter. Window length must be odd number.
    windows = [61, 81, 101, 241]
    polyo = 3
    sg_plots = []
    for i in range(0, len(windows)):
        smoothed = savgol_filter(autocorr[0], window_length=windows[i], polyorder=polyo)
        residuals = autocorr[0] - smoothed
        sg_plots.append(residuals)

    title = f"Autocorrelation Residuals - Savitzky-Golay filter. Window Lengths = {windows}. Polyorder = {polyo}"
    savefile = savefolder = k.dir_saves['images'] + os.sep + "residuals.png"
    plot_autocorrelation(autocdata=sg_plots,
                         tickinterval=60*24,
                         plottitle=title,
                         legend=windows,
                         savefile=savefile)

    savefile = savefolder = k.dir_saves['images'] + os.sep + "autocorrelation.png"
    plot_autocorrelation(autocdata=autocorr,
                         tickinterval=60*24,
                         plottitle='Autocorrelation',
                         legend=["Series"],
                         savefile=savefile)

    print(f"*** Autocorrelation completed.")
