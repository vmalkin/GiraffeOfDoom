from datetime import datetime, timezone
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
# import os
# import constants as k
# import standard_stuff
# import class_aggregator

nullvalue = np.nan


class DecimatedData:
    def __init__(self):
        self.posixtime = []
        self.seismo = []
        self.temperature = []
        self.pressure = []


def plot_data(data, dates, filename, dateformatstring):
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    plt.style.use(plotstyle)
    fig, ax = plt.subplots( layout="constrained", figsize=(200, 7), dpi=140)
    title = "Empirical Mode Decomposion - Tilt data. "

    ax.plot(dates, data, c=ink_colour[0], linewidth=1)
    ax.set_ylim([-2, 2])
    # Use proper date formatter + locator
    ax.grid(which='major', axis='x', linestyle='solid', c='black', visible='True', zorder=5)
    ax.grid(which='minor', axis='x', linestyle='dotted', c='black', visible='True', zorder=5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax.xaxis.set_minor_locator(AutoMinorLocator(6))
    plt.setp(ax.get_xticklabels(), rotation=90)  # safer than plt.xticks

    savefile = filename
    plt.savefig(savefile)
    plt.close()


def wrapper(data):
    print("*** Detrending.")
    raw_utc = []
    raw_seismo = []
    raw_temperature = []
    raw_pressure = []
    # data in format posixtime, tiltdata, temperature, pressure
    for i in range(0, len(data)):
        tim = data[i][0]
        siz = data[i][1]
        tmp = data[i][2]
        prs = data[i][3]
        raw_utc.append(tim)
        raw_seismo.append(siz)
        raw_temperature.append(tmp)
        raw_pressure.append(prs)

    # ================================================================================
    # de-mean the data. Any FFT analysis should be done immediately after this.
    demean_seismo = []
    mean_value = np.nanmean(raw_seismo)
    for item in raw_seismo:
        dd = item - mean_value
        demean_seismo.append(dd)

    demean_temperature = []
    mean_value = np.nanmean(raw_temperature)
    for item in raw_temperature:
        dd = item - mean_value
        demean_temperature.append(dd)

    demean_pressure = []
    mean_value = np.nanmean(raw_pressure)
    for item in raw_pressure:
        dd = item - mean_value
        demean_pressure.append(dd)

    # ================================================================================
    # Perform mean / z-score normalisation
    d_mu = np.mean(demean_seismo)
    d_sigma = np.std(demean_seismo)
    z_score_seismo = []
    for item in demean_seismo:
        z_score = (item - d_mu) / d_sigma
        z_score_seismo.append(z_score)

    d_mu = np.mean(demean_temperature)
    d_sigma = np.std(demean_temperature)
    z_score_temperature = []
    for item in demean_temperature:
        z_score = (item - d_mu) / d_sigma
        z_score_temperature.append(z_score)

    d_mu = np.mean(demean_pressure)
    d_sigma = np.std(demean_pressure)
    z_score_pressure = []
    for item in demean_pressure:
        z_score = (item - d_mu) / d_sigma
        z_score_pressure.append(z_score)

    # ================================================================================
    # Decimate data to plot it.
    decimate_array = []
    # seismic data is currently sampled at a rate of 10hz
    decimate_half_window = 5
    end_index = len(z_score_seismo) - decimate_half_window

    if len(z_score_seismo) > decimate_half_window:
        for i in range(0, len(z_score_seismo)):
            if decimate_half_window < i < end_index:
                px_data = raw_utc[i - decimate_half_window: i + decimate_half_window]
                sz_data = z_score_seismo[i - decimate_half_window: i + decimate_half_window]
                tm_data = z_score_temperature[i - decimate_half_window: i + decimate_half_window]
                pr_data = z_score_pressure[i - decimate_half_window: i + decimate_half_window]
                d = DecimatedData()
                d.posixtime = px_data
                d.seismo = sz_data
                d.temperature = tm_data
                d.pressure = pr_data
                decimate_array.append(d)

            else:
                decimate_array.append(nullvalue)
    else:
        for _ in data:
            decimate_array.append(nullvalue)

    # ================================================================================
    # Finally, plot data!
    print(f'Detrend completed!')
    # df = "%d  %H:%M"
    # savefile = k.dir_images['images'] + os.sep + "detrended.png"
    # plot_data(demean_seismo, raw_utc, savefile, df)



