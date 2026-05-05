import mgr_database
import standard_stuff
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np



def plot_autocorrelation(autocdata, plotcolour, plottitle, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(17, 6), dpi=140)

    # autocdata should be an array of arrays. PLot each sub-array with transparent attribute to build up the plot.
    for item in autocdata:
        ax.plot(item, c=plotcolour, linewidth=1)

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

    # ensure data is numpy array
    np_data = np.array(autocorr_prs)

    # windowed auto-correlation
    # decimate 1-second data to 1 hour
    decimated_data = []
    decimate_value = 10
    for i in range(0, len(np_data), decimate_value):
        d = np_data[i:i + decimate_value]
        mean_value = np.nanmean(d)
        decimated_data.append(mean_value)
    print(f"Length of decimated_data: {len(decimated_data)}")

    # Lag depends on the size of the decimated value. here its 30 days at 1 hr data
    lag = 6*24*7
    if len(decimated_data) < lag:
       lag = len(decimated_data)
    print(f"Length of lag: {lag}")

    # perform windowed autocorrelation.
    acorr = []
    for i in range(0, lag):
        wac_values = []
        for j in range(0, len(decimated_data) - lag):
            wac = decimated_data[i] - decimated_data[i + j]
            wac_values.append(wac)
        acorr.append(wac_values)


    # acorr should be an  array of arrays of autocorrelations.
    # Length of each sub array?
    print(f"Length of acorr: {len(acorr)}")
    for item in acorr:
        print(f"length: {len(item)}")

    plot_autocorrelation(autocdata=acorr,
                         plotcolour='blue',
                         plottitle='Autocorrelation',
                         savefile='autocorrelation.png')

    print(f"*** All analysis completed.")
