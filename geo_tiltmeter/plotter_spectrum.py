# from datetime import timezone, datetime
# import class_aggregator as aggregator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
from scipy.signal import spectrogram, detrend
from datetime import timedelta
import numpy as np
import constants as k
import os


def plot_spectrum_scipy(
    data,
    deltap,
    datetimes,
    fs,
    nfft=None,
    overlap_frac=0.75,
    fmin=None,
    fmax=None,
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

    # # --- Diurnal band extraction ---
    f0 = 1.0 / (24 * 3600)
    band = (freqs >= 0.9 * f0) & (freqs <= 1.1 * f0)
    #
    # diurnal_power = np.trapezoid(Sxx[band, :], freqs[band], axis=0)
    # diurnal_power_db = 10 * np.log10(diurnal_power + np.finfo(float).eps)

    # total_power = np.trapezoid(Sxx, freqs, axis=0)
    # diurnal_fraction = diurnal_power / total_power
    # diurnal_fraction_db = 10 * np.log10(diurnal_fraction)

    # --- Plot ---
    # fig, (ax_spec, ax_dp, ax_d) = plt.subplots(
    fig, (ax_spec) = plt.subplots(
        1, 1,
        sharex=True,
        figsize=(16, 9),
        layout="constrained",
        height_ratios=[1],
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

    # ax_spec.set_yscale("log")
    ax_spec.set_ylim(fmin, fmax)
    ax_spec.set_ylabel("Frequency (Hz)")
    fft_window_stats = f"FFT window is {round(nfft / k.sensor_reading_frequency / 60, 1)} minutes"
    subtitle = f'FFT = {nfft}. Noverlap = {noverlap}. Data Freq = {fs}Hz. {fft_window_stats}'
    ax_spec.set_title(f'{title}\n{subtitle}')
    ax_spec.grid(which='major', axis='x', linestyle='solid', c='white', visible='True', zorder=5)
    ax_spec.grid(which='minor', axis='x', linestyle='dotted', c='white', visible='True', zorder=5)
    ax_spec.axhspan(0.7 * f0, 1.3 * f0, color="cyan", alpha=0.15)
    cbar = fig.colorbar(pcm, ax=ax_spec, pad=0.01)
    cbar.set_label("Power spectral density (dB/Hz)")

    # --- Time axis formatting ---
    ax_spec.xaxis.set_major_formatter(mdates.DateFormatter(datetimeformat))
    fig.autofmt_xdate()
    ax_spec.xaxis.set_minor_locator(AutoMinorLocator(6))

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


def wrapper(utc, data):
    #  spectrographic analysis and filtering improved with ChatGPT
    print("*** Tilt Spectrogram")
    d = []
    for i in range(0, len(data)):
        try:
            j = float(data[i])
            d.append(j)
        except TypeError:
            print(data[i])

    data = detrend(d, type='linear')

    halfwindow = 60 * 30
    deltapressure = get_delta_p(data, halfwindow)
    print(f'{len(data)} {len(deltapressure)}')
    df = "%d %H:%M"
    title = "Spectrogram of tiltmeter"

    savefolder = k.dir_saves['images']
    savefile = savefolder + os.sep + "spectrum_tilt.png"

    # nfft=16384
    # nfft=32768
    # # nfft = 65536,
    # fmin = 10 ** -7,
    # fmax = 10 ** -1.8,

    plot_spectrum_scipy(
        data,
        deltap=deltapressure,
        datetimes=utc,
        fs=k.sensor_reading_frequency,
        nfft=32768,
        overlap_frac=0.75,
        fmin=10 ** -4,
        fmax=10 ** 0,
        vmin=-50,
        vmax=25,
        datetimeformat="%m %d\n%H:%M",
        title=title,
        savefile=savefile,
        cmap="inferno",
    )

