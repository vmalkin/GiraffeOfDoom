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
        self.seismo = None
        self.demean = None
        self.rollingmean = None
        self.zscore = None

    def get_noise(self):
        returnvalue = np.nan
        if len(self.seismo) > 1:
            if np.isnan(np.min(self.seismo)) is not True:
                returnvalue = np.nanmax(self.seismo) - np.min(self.seismo)
        return returnvalue


def plot_single(dateformatstring, dateobjects, data,  readings_per_tick, texttitle, savefile):
    # utcdates should be datetime objects, not POSIX floats
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    plt.style.use(plotstyle)
    fig, (ax_data) = plt.subplots(
        figsize=(50, 12),
        layout="constrained",
        height_ratios=[1, 1, 1],
    )

    # --- De-meaned seismo data ---
    ax_data.plot(dateobjects, data, c='blue', linewidth=1)
    ax_data.set_ylabel("(Arb))", color='blue')
    ax_data.tick_params(axis='y', colors='blue')
    title = "De-meaned seismic data."
    ax_data.set_title(f'{title}')
    ax_data.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_data.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    ax_data.grid(which='major', axis='y', linestyle='solid', visible='True')

    ax_data.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    fig.autofmt_xdate()
    ax_data.xaxis.set_minor_locator(AutoMinorLocator(6))

    # Use proper date formatter + locator
    ax_data.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax_data.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax_data.get_xticklabels(), rotation=45)  # safer than plt.xticks
    plt.title(f'{texttitle}')
    if savefile is not None:
        fig.savefig(savefile)
    plt.close()


def plot_multi(dateformatstring, dateobjects, data_dm, data_roll, data_zs, readings_per_tick, texttitle, savefile):
    # utcdates should be datetime objects, not POSIX floats
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    plt.style.use(plotstyle)
    fig, (ax_demean, ax_rollmean, ax_zscore) = plt.subplots(
        3, 1,
        sharex=True,
        figsize=(50, 12),
        layout="constrained",
        height_ratios=[1, 1, 1],
    )

    # --- De-meaned seismo data ---
    ax_demean.plot(dateobjects, data_dm, c='blue', linewidth=1)
    ax_demean.set_ylabel("(Arb))", color='blue')
    ax_demean.tick_params(axis='y', colors='blue')
    title = "De-meaned seismic data."
    ax_demean.set_title(f'{title}')
    ax_demean.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_demean.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    ax_demean.grid(which='major', axis='y', linestyle='solid', visible='True')

    # --- Rolling mean seismo data ---
    ax_rollmean.plot(dateobjects, data_roll, c='blue', linewidth=1)
    ax_rollmean.set_ylabel("(Arb))", color='blue')
    ax_rollmean.tick_params(axis='y', colors='blue')
    title = "Running Average."
    ax_rollmean.set_title(f'{title}')
    ax_rollmean.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_rollmean.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    ax_rollmean.grid(which='major', axis='y', linestyle='solid', visible='True')

    # --- Z-Score seismo data ---
    ax_zscore.plot(dateobjects, data_zs, c='blue', linewidth=1)
    ax_zscore.set_ylabel("(Arb))", color='blue')
    ax_zscore.tick_params(axis='y', colors='blue')
    title = "Rolling Z-Score."
    ax_zscore.set_title(f'{title}')
    ax_zscore.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_zscore.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    ax_zscore.grid(which='major', axis='y', linestyle='solid', visible='True')

    ax_zscore.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    fig.autofmt_xdate()
    ax_zscore.xaxis.set_minor_locator(AutoMinorLocator(6))

    # Use proper date formatter + locator
    ax_zscore.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax_zscore.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax_zscore.get_xticklabels(), rotation=45)  # safer than plt.xticks
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


def smoothdata(data, halfwindow):
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
                j = np.nanmean(window_data)
                j = round(j, 3)
                returnarray.append(j)
            else:
                returnarray.append(nullvalue)
    else:
        for _ in data:
            returnarray.append(nullvalue)
    return returnarray


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
    half_window = int(readings_per_second * 60 * 2)
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


    # Residual of the rolling mean on the data subtracted from the data
    # Window length ≈ cutoff period
    # Anything faster than the window → passes through
    # Anything slower → suppressed
    print('--- Rolling residual mean of data...')
    fast_data = rolling_detrended_mean(raw_seismo, halfwindow=10)
    rolling_seismo = fast_data
    # # ================================================================================
    # # # Perform a rolling mean on the data.
    # # # A rolling mean is a low-pass  filter.
    # # # Window length ≈ cutoff period
    # # # Anything slower than the window → passes through
    # # # Anything faster → suppressed
    print('--- Running Average of data...')
    residual_slow = rolling_mean(fast_data, halfwindow=1)
    # rm = rolling_mean(raw_seismo, halfwindow=half_window)
    z_score_seismo = residual_slow


    # ================================================================================
    # Decimate data to plot it.
    print('--- Decimate data to plot it...')
    decimate_array = []
    # seismic data is currently sampled at a rate of 10hz
    decimate_half_window = readings_per_second * 15
    end_index = len(raw_utc) - decimate_half_window

    for i in range(decimate_half_window, len(raw_utc) - decimate_half_window, decimate_half_window):
        if decimate_half_window < i < end_index:
            psxt = raw_utc[i - decimate_half_window: i + decimate_half_window]
            rwsz = raw_seismo[i - decimate_half_window: i + decimate_half_window]
            dmsz = demean_seismo[i - decimate_half_window: i + decimate_half_window]
            rlsz = rolling_seismo[i - decimate_half_window: i + decimate_half_window]
            zssz = z_score_seismo[i - decimate_half_window: i + decimate_half_window]

            d = DecimatedData()
            d.posixtime = psxt
            d.seismo = rwsz
            d.demean = dmsz
            d.rollingmean = rlsz
            d.zscore = zssz

            decimate_array.append(d)
            if i % 10000 == 0:
                print(f'Decimation: {i} / {len(z_score_seismo)} completed')

    # ================================================================================
    # Finally, plot data!
    print('--- Finally, plot data!...')
    df = "%d  %H:%M"
    # tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
    plot_dates = []
    plot_seismo = []
    # plot_demean = []
    # plot_rollingmean = []
    # plot_zscore = []

    for item in decimate_array:
        duration = item.posixtime[-1] - item.posixtime[0]
        if duration < ((2 * decimate_half_window + 1) * 0.1):
            time_object = np.nanmean(item.posixtime)
            time_object = datetime.fromtimestamp(time_object, tz=timezone.utc)
            seismo_current = np.nanmean(item.seismo)
            # demean_current = np.nanmean(item.demean)
            # rolling_current = np.nanmean(item.rollingmean)
            # zscore_current = np.nanmean(item.zscore)

            plot_dates.append(time_object)
            plot_seismo.append(seismo_current)
            # plot_demean.append(demean_current)
            # plot_rollingmean.append(rolling_current)
            # plot_zscore.append(zscore_current)

    plottitle = f'De-meaned, Running Avg, Z-score Normalised Data. Decimation half window: {decimate_half_window}.'
    savefile = k.dir_images['images'] + os.sep + "detrended.png"

    plot_single(dateformatstring=df,
               dateobjects=plot_dates,
               data=plot_seismo,
               readings_per_tick=60,
               texttitle=plottitle,
               savefile=savefile)

    # plot_multi(dateformatstring=df,
    #            dateobjects=plot_dates,
    #            data_dm=plot_demean,
    #            data_roll=plot_rollingmean,
    #            data_zs=plot_zscore,
    #            readings_per_tick=60,
    #            texttitle=plottitle,
    #            savefile=savefile)

    print(f'*** Detrend completed!')
