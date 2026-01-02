from datetime import timezone, datetime
from xml.etree.ElementPath import prepare_self

import constants as k
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import class_aggregator
from scipy.signal import spectrogram, detrend
from datetime import timedelta
import numpy as np


def plot_spectrum_scipy(
    data_szm,
    data_tmp,
    data_prs,
    datetimes,
    fs,
    nfft=8192,
    overlap_frac=0.75,
    fmin=1e-5,
    fmax=1e-1,
    vmin=None,
    vmax=None,
    datetimeformat="%Y-%m-%d\n%H:%M",
    title="Spectrogram",
    savefile=None,
    cmap="inferno",
):
    """
    Compute and plot a spectrogram using SciPy + Matplotlib.

    Parameters
    ----------
    data : 1D array
        Time series data (e.g. pressure or delta pressure).
    datap : 1D array
        Time series data delta pressure
    datetimes : array-like
        Datetime objects corresponding to `data`.
    fs : float
        Sampling frequency in Hz.
    nfft : int
        FFT length / segment size.
    overlap_frac : float
        Fractional overlap between segments (0–1).
    fmin, fmax : float
        Frequency limits for plotting (Hz).
    vmin, vmax : float or None
        Color scale limits in dB.
    title : str
        Plot title.
    savefile : str or None
        Output filename. If None, figure is not saved.
    cmap : str
        Matplotlib colormap.
    """

    noverlap = int(nfft * overlap_frac)

    # --- Compute spectrogram (NO plotting here) ---
    print('--- Computing spectrogram...')
    freqs, t, Sxx = spectrogram(
        data_szm,
        fs=fs,
        window="hann",
        nperseg=nfft,
        noverlap=noverlap,
        detrend="constant",
        scaling="density",
        mode="psd",
    )

    # Convert power to dB safely
    Sxx_db = 10 * np.log10(Sxx + np.finfo(float).eps)

    # --- Convert time axis to datetimes ---
    t0 = datetimes[0]
    t_dt = [t0 + timedelta(seconds=float(tt)) for tt in t]


    # --- Plot ---
    print('--- Setup for plotting...')
    fig, (ax_spec, ax_tmp, ax_prs) = plt.subplots(
        3, 1,
        sharex=True,
        figsize=(17, 12),
        layout="constrained",
        height_ratios=[2.2, 1, 1],
    )
    print('--- Plot spectrogram as colourmesh...')
    pcm = ax_spec.pcolormesh(
        t_dt,
        freqs,
        Sxx_db,
        shading="auto",
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        zorder=1
    )
    print('--- Formatting plot...')
    ax_spec.set_yscale("log")
    ax_spec.set_ylim(fmin, fmax)
    ax_spec.set_ylabel("Frequency (Hz)")
    subtitle = f'FFT = {nfft}. Noverlap = {noverlap}. Data Freq = {fs}Hz.'
    ax_spec.set_title(f'{title}\n{subtitle}')
    ax_spec.grid(which='major', axis='x', linestyle='solid', c='white', visible='True', zorder=5)
    ax_spec.grid(which='minor', axis='x', linestyle='dotted', c='white', visible='True', zorder=5)
    f0 = 10 ** -6
    ax_spec.axhspan(0.7 * f0, 1.3 * f0, color="cyan", alpha=0.15)
    cbar = fig.colorbar(pcm, ax=ax_spec, pad=0.01)
    cbar.set_label("Power spectral density (dB/Hz)")

    print('--- Adding plot annotations...')
    annotations = [
        (10, "P = 10s"),
        (100, "P = 100s"),
        (1000, "P = 16.6m"),
        (10000, "P = 2.7hr")
    ]

    x_label = t_dt[len(t_dt) // 30]  # ~3% into plot
    for period_sec, text in annotations:
        freq = 1.0 / period_sec
        # Horizontal reference line
        ax_spec.axhline(
            freq,
            color="white",
            linestyle="--",
            linewidth=1,
            alpha=0.35,
            zorder=5,
        )

        # Small label slightly above the line
        ax_spec.text(
            x_label,
            freq * 1.05,  # nudge up on log scale
            text,
            color="cyan" if period_sec >= 3600 else "white",
            fontsize=10,
            alpha=0.85,
            va="bottom",
            zorder=6,
            bbox=dict(
                boxstyle="round,pad=0.15",
                fc="black",
                ec="none",
                alpha=0.35,
            ),
        )

    print('--- Auxilliary plots for Temp and Pressure...')
    # --- plot temperature ---
    ax_tmp.plot(datetimes, data_tmp, c='red', linewidth=1)
    ax_tmp.set_ylabel("Temperature - Deg C", color='red')
    ax_tmp.tick_params(axis='y', colors='red')
    title = "Temperature"
    ax_tmp.set_title(f'{title}')
    ax_tmp.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_tmp.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    # ax_dp.grid(True, axis='both')

    # --- plot pressure ---
    ax_prs.plot(datetimes, data_prs, c='green', linewidth=1)
    ax_prs.set_ylabel("Pressure - Pa", color='green')
    ax_prs.tick_params(axis='y', colors='green')
    title = "Pressure"
    ax_prs.set_title(f'{title}')
    ax_prs.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_prs.grid(which='minor', axis='x', linestyle='dotted', visible='True')
    # ax_dp.grid(True, axis='both')

    # --- Time axis formatting ---
    ax_prs.xaxis.set_major_formatter(mdates.DateFormatter(datetimeformat))
    fig.autofmt_xdate()
    ax_prs.xaxis.set_minor_locator(AutoMinorLocator(3))

    if savefile is not None:
        fig.savefig(savefile)

    plt.close(fig)


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
                # j = window_data[-1] - window_data[0]
                j = np.nanmax(window_data) - np.nanmin(window_data)
                j = round(j, 3)
                returnarray.append(j)
            else:
                returnarray.append(nullvalue)
    else:
        for _ in data:
            returnarray.append(nullvalue)
    return returnarray


def wrapper(data):
    #  spectrographic analysis and filtering improved with ChatGPT
    print("*** Tilt Spectrogram.")
    aggregate_array = data
    # window = 10
    # aggregate_array = class_aggregator.aggregate_data(window, data)
    # aggregate_array.pop(0)
    print('--- separating data into, UTC, seismo, etc...')
    plot_utc = []
    plot_sz = []
    plot_temp = []
    plot_press = []
    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        szm = aggregate_array[i][1]
        tmp = aggregate_array[i][2]
        prs = aggregate_array[i][3]
        plot_utc.append(tim)
        plot_sz.append(szm)
        plot_temp.append(tmp)
        plot_press.append(prs)

    print('--- Initial detrend before FFT...')
    # b, a = butter(2, 0.001, btype='highpass', fs=1)
    # data = filtfilt(b, a, plot_press)
    data = detrend(plot_sz, type='linear')

    # halfwindow = 10 * 60 * 30
    # deltasz = get_delta_p(data, halfwindow)
    # # print(f'{len(data)} {len(deltasz)}')
    df = "%d %H:%M"
    title = "1 Day Spectrogram of Ground Tilt"
    savefile = k.dir_images['images'] + os.sep + "spectrum_tilt.png"
    # nfft=16384

    plot_spectrum_scipy(
        data_szm=data,
        data_tmp=plot_temp,
        data_prs=plot_press,
        datetimes=plot_utc,
        fs=10,
        nfft=16384 * 2,
        overlap_frac=0.95,
        fmin=10 ** -5.2,
        fmax=10 ** 0,
        vmin=-15,
        vmax=21,
        datetimeformat="%d\n%H:%M",
        title=title,
        savefile=savefile,
        cmap="inferno",
    )

