from datetime import datetime, timezone, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import constants as k

nullvalue = np.nan

class DecimatedData:
    def __init__(self):
        self.posixtime = None
        self.demean = None
        self.filtered = None
        # self.rollingmean = None
        # self.zscore = None

    # def get_noise(self):
    #     returnvalue = np.nan
    #     if len(self.seismo) > 1:
    #         if np.isnan(np.min(self.seismo)) is not True:
    #             returnvalue = np.nanmax(self.seismo) - np.min(self.seismo)
    #     return returnvalue


def plot_multi(dateformatstring, dateobjects, data_dm, data_filtered, readings_per_tick, texttitle, savefile):
    # utcdates should be datetime objects, not POSIX floats
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    plt.style.use(plotstyle)
    fig, (ax_demean, ax_filtered) = plt.subplots(
        2, 1,
        sharex=True,
        figsize=(18, 10),
        layout="constrained",
        height_ratios=[1, 1],
    )

    # --- De-meaned seismo data ---
    ax_demean.plot(dateobjects, data_dm, c=ink_colour[0], linewidth=1)
    ax_demean.set_ylabel("Ground Tilt. (Arb)", color=ink_colour[0])
    ax_demean.tick_params(axis='y', colors=ink_colour[0])
    title = "De-meaned seismic data."
    ax_demean.set_title(f'{title}')
    ax_demean.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_demean.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    ax_demean.grid(which='major', axis='y', linestyle='solid', visible='True')

    # --- Rolling mean seismo data ---
    ax_filtered.plot(dateobjects, data_filtered, c=ink_colour[1], linewidth=1)
    ax_filtered.set_ylabel("Amplitude of Natural Resonance. (Arb)", color=ink_colour[1])
    ax_filtered.tick_params(axis='y', colors=ink_colour[1])
    title = "Filtered."
    ax_filtered.set_title(f'{title}')
    ax_filtered.set_ylim(-0.0075, 0.0075)
    ax_filtered.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_filtered.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    ax_filtered.grid(which='major', axis='y', linestyle='solid', visible='True')

    ax_filtered.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    fig.autofmt_xdate()
    ax_filtered.xaxis.set_minor_locator(AutoMinorLocator(4))

    # Use proper date formatter + locator
    ax_filtered.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax_filtered.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax_filtered.get_xticklabels(), rotation=45)  # safer than plt.xticks
    plt.title(f'{texttitle}')
    if savefile is not None:
        fig.savefig(savefile)
    plt.close()


def demean_data(datarray):
    return_array = []
    mean_value = np.nanmean(datarray)
    for item in datarray:
        dd = item - mean_value
        return_array.append(dd)
    return return_array


def rolling_mean(dataarray, halfwindow):
    rolling_array = []
    end_index = len(dataarray) - halfwindow
    for i in range(0, len(dataarray)):
        if halfwindow < i < end_index:
            d_mean = np.mean(dataarray[i - halfwindow: i + halfwindow])
            rolling_array.append(d_mean)
        else:
            rolling_array.append(np.nan)
        if i % 1000 == 0:
            print(f'--- Rolling Mean: {i} / {len(dataarray)} completed')
    return rolling_array


def rolling_detrended_mean(dataarray, halfwindow):
    rolling_array = []
    end_index = len(dataarray) - halfwindow
    for i in range(0, len(dataarray)):
        if halfwindow < i < end_index:
            d_mean = np.mean(dataarray[i - halfwindow: i + halfwindow])
            d = dataarray[i] - d_mean
            rolling_array.append(d)
        else:
            rolling_array.append(np.nan)
        if i % 1000 == 0:
            print(f'--- Rolling Residual of Detrended Mean: {i} / {len(dataarray)} completed')
    return rolling_array


def get_delta_p(data, halfwindow):
    nullvalue = np.nan
    returnarray = []
    end_index = len(data) - halfwindow
    # we want to return an array the same size as the input array. We pad the beginning and end with
    # null values. The array is split up thus:
    # [half window at start] <-> [data we work on] <-> [half window at end]
    # IF we were doing a running avg for instance, this would give us a window centred on our chosen data. THis is
    # preferred
    if len(data) > halfwindow:
        for i in range(0, len(data)):
            if halfwindow < i < end_index:
                window_data = data[i - halfwindow: i + halfwindow]
                j = window_data[-1] - window_data[0]
                j = round(j, 3)
                returnarray.append(j)
            else:
                returnarray.append(nullvalue)
    else:
        for _ in data:
            returnarray.append(nullvalue)
    return returnarray


# ================================================================================
def wrapper(data):
    print("*** Detrend started.")
    # Our window should relate to real phenomena based on detected events. An hour or so is often used
    # for seismic events
    readings_per_second = 10
    raw_utc = []
    raw_seismo = []

    # data in format posixtime, tiltdata, temperature, pressure
    for i in range(0, len(data)):
        tim = data[i][0]
        siz = data[i][1]
        raw_utc.append(tim)
        raw_seismo.append(siz)

    # ================================================================================
    # de-mean the data. Any FFT analysis should be done immediately after this.
    print('--- De-meaning...')
    demean_seismo = demean_data(raw_seismo)

    # ================================================================================
    # Process data to display when the pendulum is exited at it's natural frequency
    detrended_10sec_under = rolling_detrended_mean(demean_seismo, halfwindow=int(readings_per_second * 1.5))
    detrended_1sec_under = rolling_detrended_mean(demean_seismo, halfwindow=int(readings_per_second * 0.5))

    filtered = []
    for i in range(0, len(detrended_10sec_under)):
        j = detrended_10sec_under[i] - detrended_1sec_under[i]
        filtered.append(j)
    # filtered = rolling_mean(filtered, halfwindow=readings_per_second * 60)
    # filtered = rolling_mean(filtered, halfwindow=readings_per_second * 60)

    # ================================================================================
    # Decimate data to plot it.
    print('--- Decimate data to plot it...')
    decimate_array = []
    # seismic data is currently sampled at a rate of 10hz
    halfwindow_width_seconds = 60
    decimate_half_window = readings_per_second * halfwindow_width_seconds
    end_index = len(raw_utc) - decimate_half_window

    for i in range(decimate_half_window, len(raw_utc) - decimate_half_window, decimate_half_window):
        if decimate_half_window < i < end_index:
            psxt = raw_utc[i - decimate_half_window: i + decimate_half_window]
            dm = demean_seismo[i - decimate_half_window: i + decimate_half_window]
            fltr = filtered[i - decimate_half_window: i + decimate_half_window]
            # rlsz = rolling_seismo[i - decimate_half_window: i + decimate_half_window]
            # zssz = z_score_seismo[i - decimate_half_window: i + decimate_half_window]

            d = DecimatedData()
            d.posixtime = psxt
            d.filtered = fltr
            d.demean = dm
            # d.rollingmean = rlsz
            # d.zscore = zssz

            decimate_array.append(d)
            if i % 10000 == 0:
                print(f'Decimation: {i} / {len(raw_utc)} completed')

    # ================================================================================
    # Finally, plot data!
    print('--- Finally, plot data!...')
    df = "%d  %H:%M"
    # tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
    plot_dates = []
    plot_demean = []
    plot_filtered = []
    # plot_rollingmean = []
    # plot_zscore = []

    for item in decimate_array:
        duration = item.posixtime[-1] - item.posixtime[0]
        if duration < ((2 * decimate_half_window + 1) * 0.1):
            time_object = np.nanmean(item.posixtime)
            time_object = datetime.fromtimestamp(time_object, tz=timezone.utc)
            demean_current = np.nanmean(item.demean)
            filtered_current = np.nanmean(item.filtered)
            # rolling_current = np.nanmean(item.rollingmean)
            # zscore_current = np.nanmean(item.zscore)

            plot_dates.append(time_object)
            plot_demean.append(demean_current)
            plot_filtered.append(filtered_current)
            # plot_rollingmean.append(rolling_current)
            # plot_zscore.append(zscore_current)

    plottitle = f'Filtered natural resonance. Decimation window: {2 * halfwindow_width_seconds} seconds.'
    savefile = k.dir_images['images'] + os.sep + "resonance.png"

    plot_multi(dateformatstring=df,
               dateobjects=plot_dates,
               data_dm=plot_demean,
               data_filtered=plot_filtered,
               readings_per_tick=60,
               texttitle=plottitle,
               savefile=savefile)

    print(f'*** Detrend completed!')
