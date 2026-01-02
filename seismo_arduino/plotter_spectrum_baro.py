from datetime import timezone, datetime
import constants as k
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import class_aggregator
from scipy.signal import spectrogram, detrend
from datetime import timedelta
import numpy as np
import standard_stuff


def plot_spectrum_scipy(
    data,
    deltap,
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
    freqs, t, Sxx = spectrogram(
        data,
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

    # --- Diurnal band extraction ---
    f0 = 1.0 / (24 * 3600)
    band = (freqs >= 0.9 * f0) & (freqs <= 1.1 * f0)

    diurnal_power = np.trapezoid(Sxx[band, :], freqs[band], axis=0)
    diurnal_power_db = 10 * np.log10(diurnal_power + np.finfo(float).eps)

    # total_power = np.trapezoid(Sxx, freqs, axis=0)
    # diurnal_fraction = diurnal_power / total_power
    # diurnal_fraction_db = 10 * np.log10(diurnal_fraction)

    # --- Plot ---
    fig, (ax_spec, ax_dp, ax_d) = plt.subplots(
        3, 1,
        sharex=True,
        figsize=(17, 12),
        layout="constrained",
        height_ratios=[2.2, 1, 1],
    )

    pcm = ax_spec.pcolormesh(
        t_dt,
        freqs,
        Sxx_db,
        shading="auto",
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )

    ax_spec.set_yscale("log")
    ax_spec.set_ylim(fmin, fmax)
    ax_spec.set_ylabel("Frequency (Hz)")
    subtitle = f'FFT = {nfft}. Noverlap = {noverlap}. Data Freq = {fs}Hz.'
    ax_spec.set_title(f'{title}\n{subtitle}')
    ax_spec.grid(which='major', axis='x', linestyle='solid', c='white', visible='True', zorder=5)
    ax_spec.grid(which='minor', axis='x', linestyle='dotted', c='white', visible='True', zorder=5)
    ax_spec.axhspan(0.7 * f0, 1.3 * f0, color="cyan", alpha=0.15)
    cbar = fig.colorbar(pcm, ax=ax_spec, pad=0.01)
    cbar.set_label("Power spectral density (dB/Hz)")

    annotations = [
        (100, "100 sec\nMostly noise."),
        (16 * 60, "16 min\nMesoscale variability."),
        (2.7 * 3600, "2.7 hr\nSynoptic-mesoscale transition."),
        (27 * 3600, "27 hr\nRegion of diurnal atmospheric tide (S1)."),
    ]

    for period_sec, text in annotations:
        freq = 1.0 / period_sec
        ax_spec.annotate(
            text,
            xy=(t_dt[0], freq),
            fontsize=8,
            bbox=dict(boxstyle="round", fc="1", ec="black"),
        )
    # --- Pressure Delta ---
    ax_dp.plot(datetimes, deltap, c='blue', linewidth=1)
    ax_dp.set_ylabel("Δ Pressure (Pa) - 1hr window", color='blue')
    ax_dp.tick_params(axis='y', colors='blue')
    title = "Hourly pressure change emphasizes transient synoptic forcing while suppressing slowly varying components such as the diurnal tide."
    ax_dp.set_title(f'{title}')
    ax_dp.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_dp.grid(which='minor', axis='x', linestyle='dotted', visible='True')

    # --- Pressure Delta 2 ---
    halfwindow = 60 * 120
    dp = get_delta_p(data, halfwindow)
    ax_d.plot(datetimes, dp, c='red', linewidth=1)
    ax_d.set_ylabel("Δ Pressure (Pa) - 4hr window", color='red')
    ax_d.tick_params(axis='y', colors='red')
    title = "Synoptic evolution."
    ax_d.set_title(f'{title}')
    ax_d.grid(which='major', axis='x', linestyle='solid', visible='True')
    ax_d.grid(which='minor', axis='x', linestyle='dotted', visible='True')

    # --- Time axis formatting ---
    ax_d.xaxis.set_major_formatter(mdates.DateFormatter(datetimeformat))
    fig.autofmt_xdate()
    ax_d.xaxis.set_minor_locator(AutoMinorLocator(6))

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
                j = window_data[-1] - window_data[0]
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
    print("*** Barometric Spectrogram")
    window = 10
    aggregate_array = class_aggregator.aggregate_data(window, data)
    aggregate_array.pop(0)

    plot_utc = []
    plot_press = []
    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
        plot_utc.append(tim)
        plot_press.append(prs)

    # b, a = butter(2, 0.001, btype='highpass', fs=1)
    # data = filtfilt(b, a, plot_press)
    data = detrend(plot_press, type='linear')

    halfwindow = 60 * 30
    deltapressure = get_delta_p(data, halfwindow)
    print(f'{len(data)} {len(deltapressure)}')
    df = "%d %H:%M"
    title = "Spectrogram of Barometric Pressure"
    savefile = k.dir_images['images'] + os.sep + "spectrum_press.png"
    # nfft=16384
    # nfft=32768

    plot_spectrum_scipy(
        data,
        deltap=deltapressure,
        datetimes=plot_utc,
        fs=1,
        nfft=32768,
        overlap_frac=0.75,
        fmin=10**-5.2,
        fmax=10**-1.8,
        vmin=5,
        vmax=90,
        datetimeformat="%d\n%H:%M",
        title=title,
        savefile=savefile,
        cmap="inferno",
    )

