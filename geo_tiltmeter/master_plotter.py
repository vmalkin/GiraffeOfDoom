import mgr_database
import standard_stuff
import plotter_spectrum_baro
import plotter_dual
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import os
import constants as k


def plot_singledata(dateformatstring, dateobjects, singledataarray, tickinterval, plotcolour, plottitle, savefile):
    plt.style.use('bmh')
    fig, ax = plt.subplots(layout="constrained", figsize=(48, 6), dpi=140)
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
    print(f"*** BEGIN analysis.")
    end_time = time.time()
    start_time = end_time - 86400
    data = mgr_database.db_data_get(start_time, end_time)

    print(f"*** Data downloaded from DB.")

    # process data, times for plotting.
    # data_prs = []
    data_tilt = []
    data_utc = []
    for psx, tilt in data:
    # for psx, temp, prs in autocorr_data:
    #     data_prs.append(prs)
        data_tilt.append(tilt)
        tim = datetime.fromtimestamp(psx, tz=timezone.utc)  # datetime object
        # print(tim)
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

    print(f"*** Temp and pressure plots completed.")

    plotter_spectrum_baro.wrapper(data_utc, data_tilt)
    plotter_dual.wrapper(data_utc, data_tilt)

    print(f"*** All analysis completed.")
