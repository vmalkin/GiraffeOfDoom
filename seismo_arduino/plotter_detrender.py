from datetime import datetime, timezone, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import constants as k
import standard_stuff


nullvalue = np.nan


class DecimatedData:
    def __init__(self):
        self.posixtime = []
        self.seismo = []
        self.temperature = []
        self.pressure = []

    def get_noise(self):
        returnvalue = np.nan
        if len(self.seismo) > 1:
            if np.isnan(np.min(self.seismo)) is not True:
                returnvalue = np.nanmax(self.seismo) - np.min(self.seismo)
        return returnvalue


def plot_multi(dateformatstring, dateobjects, dataarrays, readings_per_tick, texttitle, savefile):
    # utcdates should be datetime objects, not POSIX floats
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    plt.style.use(plotstyle)
    # fig, ax1 = plt.subplots(nrows=2, layout="constrained", figsize=(16, 8), dpi=140)
    fig, (ax_top, ax_bottom) = plt.subplots(
        2, 1, figsize=(16, 8), dpi=140, sharex=True, height_ratios=[2, 1]
    )

    # Subplots with separate y axes
    ax_top.plot(dateobjects, dataarrays[0], c=ink_colour[0], linewidth=1)
    ax_top.set_ylabel("Tiltmeter (Arb). StdDev.", color=ink_colour[0])
    ax_top.tick_params(axis='y', colors=ink_colour[0])

    ax_top2 = ax_top.twinx()
    ax_top2.plot(dateobjects, dataarrays[1], c=ink_colour[1], linewidth=1)
    ax_top2.set_ylabel("Pressure (Pa). StdDev.", color=ink_colour[1])
    ax_top2.tick_params(axis='y', colors=ink_colour[1])
    ax_top2.spines['right'].set_position(('outward', 60))
    ax_top2.yaxis.grid(False)

    ax_top3 = ax_top.twinx()
    ax_top3.plot(dateobjects, dataarrays[2], c=ink_colour[2], linewidth=1)
    ax_top3.set_ylabel("Temperature (°C). StdDev.", color=ink_colour[2])
    ax_top3.tick_params(axis='y', colors=ink_colour[2])
    ax_top3.yaxis.grid(False)

    noise_colour = '#505050'
    ax_bottom.plot(dateobjects, dataarrays[3], c=noise_colour, linewidth=0.8)
    ax_bottom.set_ylabel("Tilt Noise. (Arb).", color=noise_colour)
    ax_bottom.tick_params(axis='y', colors=noise_colour)
    ax_bottom.set_ylim([3, 15])
    ax_bottom.yaxis.grid(False)

    # Use proper date formatter + locator
    ax_top.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax_top.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax_bottom.get_xticklabels(), rotation=90)  # safer than plt.xticks
    plot_title = texttitle
    ax_top.set_title(plot_title)
    plt.tight_layout()
    plt.savefig(savefile)
    plt.close()


def wrapper(data):
    print("*** Detrend started.")
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
    print('--- De-meaning...')
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
    print('--- Perform mean / z-score normalisation...')
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
    print('--- Decimate data to plot it...')
    decimate_array = []
    # seismic data is currently sampled at a rate of 10hz
    decimate_half_window = 5 * 30
    end_index = len(z_score_seismo) - decimate_half_window

    for i in range(0, len(z_score_seismo), decimate_half_window * 2):
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
            if i % 10000 == 0:
                print(f'{i} / {len(z_score_seismo)} completed')

    # ================================================================================
    # Finally, plot data!
    print('--- Finally, plot data!...')
    df = "%d  %H:%M"
    # tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
    plot_dates = []
    datawrapper = []
    plot_seismo = []
    plot_temperature = []
    plot_pressure = []
    plot_noise = []

    for item in decimate_array:
        duration = item.posixtime[-1] - item.posixtime[0]
        if duration < ((2 * decimate_half_window + 1) * 0.1):
            time_object = np.nanmean(item.posixtime)
            time_object = datetime.fromtimestamp(time_object, tz=timezone.utc)
            seismo_current = np.nanmean(item.seismo)
            temperature_current = np.nanmean(item.temperature)
            pressure_current = np.nanmean(item.pressure)
            noise = item.get_noise()

            plot_dates.append(time_object)
            plot_seismo.append(seismo_current)
            plot_temperature.append(temperature_current)
            plot_pressure.append(pressure_current)
            plot_noise.append(noise)

    datawrapper.append(plot_seismo)
    datawrapper.append(plot_pressure)
    datawrapper.append(plot_temperature)
    datawrapper.append(plot_noise)

    plottitle = f'De-meaned, Z-score Normalised Data. Decimation half window: {decimate_half_window}.'
    savefile = k.dir_images['images'] + os.sep + "detrended.png"
    plot_multi(dateformatstring=df,
               dateobjects=plot_dates,
               dataarrays=datawrapper,
               readings_per_tick=60 * 6,
               texttitle=plottitle,
               savefile=savefile)

    print(f'*** Detrend completed!')



