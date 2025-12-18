from datetime import timezone, datetime
import constants as k
import matplotlib.pyplot as plt
import os
import class_aggregator
from scipy.signal import spectrogram, detrend
from datetime import timedelta
import numpy as np


def plot_spectrum_scipy(
    data,
    datetimes,
    fs,
    nfft=8192,
    overlap_frac=0.75,
    fmin=1e-5,
    fmax=1e-1,
    vmin=None,
    vmax=None,
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

    # --- Plot ---
    fig, (ax_spec, ax_ts) = plt.subplots(
        2, 1,
        sharex=True,
        figsize=(17, 9),
        layout="constrained",
        height_ratios=[2, 1],
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
    ax_spec.set_title(title)
    cbar = fig.colorbar(pcm, ax=ax_spec, pad=0.01)
    cbar.set_label("Power spectral density (dB/Hz)")

    annotations = [
        (100, "100 sec\nMostly noise"),
        (16 * 60, "16 min\nMesoscale"),
        (2.7 * 3600, "2.7 hr\nSynoptic"),
        (27 * 3600, "27 hr\nSynoptic"),
    ]

    for period_sec, text in annotations:
        freq = 1.0 / period_sec
        ax_spec.annotate(
            text,
            xy=(t_dt[0], freq),
            fontsize=8,
            bbox=dict(boxstyle="round", fc="1", ec="black"),
        )

    ax_ts.plot(t_dt, data, c='blue', linewidth=2)

    if savefile is not None:
        fig.savefig(savefile)

    plt.close(fig)


def wrapper(data):
    #  spectrographic analysis and filtering improved with ChatGPT
    print("*** Barometric Spectrogram - Past 24 hours")
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

    df = "%d %H:%M"
    title = "Spectrogram of Barometric Pressure"
    savefile = k.dir_images['images'] + os.sep + "spectrum_press.png"
    # tick = 60 * 60 * 12

    plot_spectrum_scipy(
        data,
        plot_utc,
        fs=1,
        nfft=8192,
        overlap_frac=0.75,
        fmin=10**-5,
        fmax=10**-1.8,
        vmin=5,
        vmax=80,
        title=title,
        savefile=savefile,
        cmap="inferno",
    )

