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



def plot_autocorrelation(autocdata, tickinterval, plotcolour, plottitle, legend, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(19, 6), dpi=140)
    plotcolours = ["#003049", "#d62828", "#f77f00"]
    for i in range(0, len(autocdata)):
        ax.plot(autocdata[i], c=plotcolours[i], linewidth=2)

    ax.xaxis.set_major_locator(plt.MultipleLocator(tickinterval))
    # ax.set_ylim([-0.02, 0.02])
    plt.legend(legend, loc='lower center')
    plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks
    plot_title = plottitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax.set_title(plot_title)
    plt.tight_layout()
    plt.savefig(savefile)
    plt.close()


def plot_singledata(dateformatstring, dateobjects, singledataarray, tickinterval, plotcolour, plottitle, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(19, 6), dpi=140)
    ax.plot(dateobjects, singledataarray, c=plotcolour, linewidth=1)

    # Use proper date formatter + locator
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=tickinterval))
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

    sanitised_list = np.array(sanitised_list)
    posix_data = sanitised_list[:, 0]
    seis_data = sanitised_list[:, 1]
    temp_data = sanitised_list[:, 2]
    pressure_data = sanitised_list[:, 3]
    # detrend the seismic data
    seis_data = detrend(seis_data, type='linear')

    # Compute autocorrelation
    # https://www.scicoding.com/4-ways-of-calculating-autocorrelation-in-python/
    # Mean
    mean = np.mean(seis_data)

    # Variance
    var = np.var(seis_data)

    # Normalized data
    decimated_data = seis_data - mean
    ac = np.correlate(decimated_data, decimated_data, mode='full')[len(decimated_data)-1:]
    ac = ac / var / len(decimated_data)
    autocorr = []
    autocorr.append(ac)

    # Compute residuals using a Savitzky Golay Filter. Window length must be odd number.
    windows = [61, 81, 101]
    polyo = 3
    sg_plots = []
    for i in range(0, len(windows)):
        smoothed = savgol_filter(autocorr[0], window_length=windows[i], polyorder=polyo)
        residuals = autocorr[0] - smoothed
        sg_plots.append(residuals)

    title = f"Autocorrelation Residuals - Savitzky-Golay filter. Window Lengths = {windows}. Polyorder = {polyo}"
    savefile = f"residuals.png"
    plot_autocorrelation(autocdata=sg_plots,
                         tickinterval=24,
                         plotcolour=(0.5, 0.2, 0.5),
                         plottitle=title,
                         legend=windows,
                         savefile=savefile)

    plot_autocorrelation(autocdata=autocorr,
                         tickinterval=24,
                         plotcolour=(0.1, 0.2, 0.5),
                         plottitle='Autocorrelation',
                         legend=["Series"],
                         savefile='autocorrelation.png')

    print(f"*** Autocorrelation completed.")
