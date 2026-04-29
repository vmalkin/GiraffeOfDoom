import mgr_database
import standard_stuff
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


if __name__ == "__main__":
    end_time = time.time()
    # print("Start time:", standard_stuff.posix2utc(1777442234.41846, timeformat='%Y-%m-%d %H:%M:%S'))
    start_time = end_time - 86400

    data = mgr_database.db_data_get(start_time, end_time)
    print(f"Data length: {len(data)}")
    for psx, temp, prs in data:
        print(f"{standard_stuff.posix2utc(psx, timeformat='%Y-%m-%d %H:%M:%S')},{temp},{prs}")
        # print(f"{psx},{temp},{prs}")


def plot_multi(dateformatstring, dateobjects, dataarrays, readings_per_tick, texttitle, savefile):
    ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
    plotstyle = 'bmh'
    # utcdates should be datetime objects, not POSIX floats
    plt.style.use(plotstyle)
    # fig, ax1 = plt.subplots(nrows=2, layout="constrained", figsize=(16, 8), dpi=140)
    fig, (ax_top, ax_bottom) = plt.subplots(
        2, 1, figsize=(16, 8), dpi=140, sharex=True, height_ratios=[1, 1]
    )

    # Subplots with separate y axes
    ax_top.plot(dateobjects, dataarrays[0], c=ink_colour[0], linewidth=1)
    ax_top.set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
    ax_top.tick_params(axis='y', colors=ink_colour[0])
    limits = minmaxes(dataarrays[0])
    ax_top.set_ylim(limits)

    # ax_top2 = ax_top.twinx()
    # ax_top2.plot(dateobjects, dataarrays[1], c=ink_colour[1], linewidth=1)
    # ax_top2.set_ylabel("Pressure. Pa.", color=ink_colour[1])
    # ax_top2.tick_params(axis='y', colors=ink_colour[1])
    # limits = minmaxes(dataarrays[1])
    # ax_top2.set_ylim(limits)
    # ax_top2.spines['right'].set_position(('outward', 60))
    # ax_top2.yaxis.grid(False)
    #
    # ax_top3 = ax_top.twinx()
    # ax_top3.plot(dateobjects, dataarrays[2], c=ink_colour[2], linewidth=1)
    # ax_top3.set_ylabel("Temperature. Deg C.", color=ink_colour[2])
    # ax_top3.tick_params(axis='y', colors=ink_colour[2])
    # limits = minmaxes(dataarrays[2])
    # ax_top3.set_ylim(limits)
    # ax_top3.yaxis.grid(False)

    noise_colour = '#505050'
    ax_bottom.plot(dateobjects, dataarrays[3], c=noise_colour, linewidth=0.8)
    # ax_bottom.bar(dateobjects, dataarrays[3], width=0.001, color=noise_colour)
    ax_bottom.set_ylabel("Noise - Arbitrary Units.", color=noise_colour)
    ax_bottom.tick_params(axis='y', colors=noise_colour)
    title = "Noise: max(decimated data) - min(decimated data)."
    ax_bottom.set_title(f'{title}')
    # limits = minmaxes(dataarrays[3])
    ax_bottom.set_ylim([3, 16])
    # ax_bottom.spines['right'].set_position(('outward', 110))
    ax_bottom.yaxis.grid(False)

    # Use proper date formatter + locator
    ax_top.xaxis.set_major_formatter(mdates.DateFormatter(dateformatstring))
    ax_top.xaxis.set_major_locator(mdates.MinuteLocator(interval=readings_per_tick))
    plt.setp(ax_bottom.get_xticklabels(), rotation=90)  # safer than plt.xticks
    plot_title = texttitle + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    ax_top.set_title(plot_title)
    plt.tight_layout()
    plt.savefig(savefile)
    plt.close()


def minmaxes(dataarray):
    data_max = np.nanmax(dataarray)
    data_min = np.nanmin(dataarray)
    print(f'Min maxes are: {data_min} and {data_max}')
    if data_max is np.nan:
        if data_min is np.nan:
            return []
    else:
        padding = (data_max - data_min) / 10
        return [data_min - padding, data_max + padding]