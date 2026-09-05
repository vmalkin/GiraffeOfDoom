import mgr_database
import standard_stuff
import plotter_spectrum
import plotter_dual
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import os
import constants as k


def plot_singledata(dateformatstring, dateobjects, singledataarray, tickinterval, plotcolour, plottitle, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(16, 8), dpi=140)
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
    print("Custom date-range query.\n")
    yyyy_start = input("Enter YYYY start: ")
    mm_start = input("Enter MM start: ")
    dd_start = input("Enter DD start: ")
    hh_start = input("Enter HH start: ")
    print("\n")
    yyyy_end = input("Enter YYYY end: ")
    mm_end = input("Enter MM end: ")
    dd_end = input("Enter DD end: ")
    hh_end = input("Enter HH end: ")

    # '%Y-%m-%d %H'
    utc_start = f"{yyyy_start}-{mm_start}-{dd_start} {hh_start}"
    utc_end = f"{yyyy_end}-{mm_end}-{dd_end} {hh_end}"

    psx_start = standard_stuff.utc2posix(utc_start, '%Y-%m-%d %H')
    psx_end = standard_stuff.utc2posix(utc_end, '%Y-%m-%d %H')

    print(f"UTC/PSX start: {utc_start} / {psx_start}")
    print(f"UTC/PSX end: {utc_end} / {psx_end}")

    print(f"*** BEGIN plots.")
    data = mgr_database.db_data_get(psx_start, psx_end)
    print(f"*** Data downloaded from DB. Length: {len(data)}")

    data_tilt = []
    data_utc = []
    for psx, tilt in data:
        data_tilt.append(tilt)
        tim = datetime.fromtimestamp(psx, tz=timezone.utc)  # datetime object
        data_utc.append(tim)

    savefolder = k.dir_saves['images']
    savefile = savefolder + os.sep + "basic_tilt.png"
    plot_singledata(dateformatstring='%Y-%m-%d %H:%M',
                    dateobjects=data_utc,
                    singledataarray=data_tilt,
                    tickinterval=60,
                    plotcolour='red',
                    plottitle='Todays tilt data',
                    savefile=savefile)

    plotter_spectrum.wrapper(data_utc, data_tilt)
    # plotter_dual.wrapper(data_utc, data_tilt)
    # plotter_fft_movie.wrapper(data_utc, data_tilt)

    print(f"*** All plots completed.")
