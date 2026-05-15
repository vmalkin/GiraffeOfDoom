import mgr_database
import standard_stuff
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np
from scipy.signal import savgol_filter



def plot_autocorrelation(autocdata, tickinterval, plotcolour, plottitle, legend, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(17, 6), dpi=140)
    plotcolours = ["#003049", "#d62828", "#f77f00"]
    for i in range(0, len(autocdata)):
        ax.plot(autocdata[i], c=plotcolours[i], linewidth=2)

    ax.xaxis.set_major_locator(plt.MultipleLocator(tickinterval))
    plt.legend(legend, loc='lower center')
    plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks
    plot_title = plottitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax.set_title(plot_title)
    plt.tight_layout()
    plt.savefig(savefile)
    plt.close()


def plot_singledata(dateformatstring, dateobjects, singledataarray, tickinterval, plotcolour, plottitle, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(17, 6), dpi=140)
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
    print(f"*** BEGIN analysis.")
    end_time = time.time()
    start_time = end_time - 86400
    data = mgr_database.db_data_get(start_time, end_time)

    # Set up for auto-correlation. At least 60 days.
    autocorr_start_time = end_time - (86400 * 60)
    # end time is already defined
    autocorr_data = mgr_database.db_data_get(autocorr_start_time, end_time)

    print(f"*** Data downloaded from DB.")

    # process data, times for plotting.
    data_prs = []
    data_temp = []
    data_utc = []
    for psx, temp, prs in data:
    # for psx, temp, prs in autocorr_data:
        data_prs.append(prs)
        data_temp.append(temp)
        tim = datetime.fromtimestamp(psx, tz=timezone.utc)  # datetime object
        data_utc.append(tim)

    plot_singledata(dateformatstring='%Y-%m-%d %H:%M',
                    dateobjects=data_utc,
                    singledataarray=data_temp,
                    tickinterval=60,
                    plotcolour='red',
                    plottitle='Todays Temperature',
                    savefile='temperature.png')

    plot_singledata(dateformatstring='%Y-%m-%d %H:%M',
                    dateobjects=data_utc,
                    singledataarray=data_prs,
                    tickinterval=60,
                    plotcolour='green',
                    plottitle='Todays Pressure',
                    savefile='pressure.png')

    print(f"*** Temp and pressure plots completed.")

    autocorr_prs = []
    for psx, temp, prs in autocorr_data:
        autocorr_prs.append(prs)

    # # ensure data is numpy array
    # np_data = np.array(autocorr_prs)

    # windowed auto-correlation
    # decimate 1-second data to 1 hour
    decimated_data = []
    decimate_value = 60*60
    for i in range(0, len(autocorr_prs), decimate_value):
        try:
            d = autocorr_prs[i:i + decimate_value]
            mean_value = np.nanmean(d)
            decimated_data.append(mean_value)
        except:
            print(f"Currupted value: {d}")
    print(f"Length of decimated_data: {len(decimated_data)}")

    # Compute autocorrelation
    # https://www.scicoding.com/4-ways-of-calculating-autocorrelation-in-python/
    # Mean
    mean = np.mean(decimated_data)

    # Variance
    var = np.var(decimated_data)

    # Normalized data
    decimated_data = decimated_data - mean
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



    print(f"*** All analysis completed.")
