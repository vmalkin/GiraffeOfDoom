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
    ax.plot(autocdata, c=plotcolour, linewidth=1)
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
    end_time = time.time()
    start_time = end_time - 86400
    data = mgr_database.db_data_get(start_time, end_time)

    # Set up for auto-correlation. At least 60 days.
    autocorr_start_time = end_time - (86400 * 60)
    # end time is already defined
    autocorr_data = mgr_database.db_data_get(autocorr_start_time, end_time)

    # process data, times for plotting.
    data_prs = []
    data_temp = []
    data_utc = []
    for psx, temp, prs in data:
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



    data_prs = []
    for psx, temp, prs in autocorr_data:
        data_prs.append(prs)

    # ensure data is numpy array
    np_data = np.array(data_prs)

    # Mean
    mean = np.mean(np_data)

    # Variance
    var = np.var(np_data)

    # Normalized data
    ndata = np_data - mean

    acorr = np.correlate(ndata, ndata, 'full')[len(ndata)-1:]
    acorr = acorr / var / len(ndata)

    plot_autocorrelation(autocdata=acorr,
                         plotcolour='blue',
                         plottitle='Autocorrelation',
                         savefile='autocorrelation.png')

