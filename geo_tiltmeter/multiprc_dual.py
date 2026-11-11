# This template uses multiprocessing to iterate over very large arrays of data. We will use the
# ProcessPoolExecutor as it's considered the more modern method.
# Yes - AI has helped me with the ideas, but as you can tell by the janky code, that bit is mine.
#
# For the multiprocessing to work tHis script MUST be called from another script that has
# it's own if __name__ == '__main__'
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
import class_aggregator
import standard_stuff
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates
import time
import os
import constants as k
import numpy as np


# There may be other functions here called by process_chunk
ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_dual_hourly(
        df,
        utctimes,
        data,
        title,
        filename,
        ddminmax
    ):

    plt.style.use(plotstyle)
    fig, ax = plt.subplots(1, layout="constrained", figsize=(16, 4), dpi=250)
    # utcdates should be datetime objects, not POSIX floats
    ax.plot(utctimes, data, c=ink_colour[0], linewidth=1)
    ax.set_ylabel("Tiltmeter. Arbitrary Units.", color=ink_colour[0])
    ax.set_ylim(ddminmax)
    my_fmt = mdates.DateFormatter(df)
    ax.xaxis.set_major_formatter(my_fmt)
    # Major grid
    ax.grid(which='major', linestyle=':', color='black', alpha=1)
    ax.grid(which='minor', linestyle=':', color='black',alpha=0.5)
    # Minor ticks and grid
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(1))

    # # ax[1] = ax1.twinx()
    # ax[1].plot(utctimes, data_dx, c=ink_colour[1], linewidth=1)
    # ax[1].set_ylabel("Tilt, dx/dt", color=ink_colour[1])
    # ax[1].set_ylim(dxminmax)
    # my_fmt = mdates.DateFormatter(df)
    # ax[1].xaxis.set_major_formatter(my_fmt)
    # # Major grid
    # ax[1].grid(which='major', linestyle=':', color='black', alpha=1)
    # ax[1].grid(which='minor', linestyle=':', color='black',alpha=0.5)
    # # Minor ticks and grid
    # ax[1].xaxis.set_minor_locator(AutoMinorLocator(5))
    # ax[1].yaxis.set_minor_locator(AutoMinorLocator(1))

    plot_title = title + " - " + standard_stuff.posix2utc(time.time(), '%Y-%m-%d %H:%M')
    plt.xlabel("UTC Datetime.")
    fig.suptitle(plot_title)
    # filename = utctimes[len(utctimes) - 1].strftime('%Y-%m-%d-%H-%M')
    savefile = k.dir_saves['images'] + os.sep + str(filename) + ".png"
    plt.savefig(savefile)
    plt.close()
    print(f"Dualplotter: {savefile}")


def process_chunk(chunk):
    # This is a _Worker_ which typically uses the chunk to process then generate a
    # single plot from this chunk. Return the filename of the plot.
    # Data is in form [utctimes, seismo_data, dx_data].
    if chunk is not None:
        df = "%b %d \n%H:%M"
        title = f'Tiltmeter One Day. Data and dx/dt.'
        savefolder = k.dir_saves['images']
        plot_dual_hourly(
            df=df,
            utctimes=chunk[0],
            data=chunk[1],
            title=title,
            filename=chunk[2],
            ddminmax=chunk[3]
        )
        return None


def chunks(utcobj, data, chunkstep, chunklength, ddminmax):
    # In Python, yield turns a normal function into a generator so
    # it can produce values one at a time instead of returning everything at once.
    # Each time the generator runs up to a yield, it pauses and gives the value to
    # the caller, then continues later from where it left off. THis memory efficient
    # Here we are stepping BACKWARDS so most recent data is plotted.
    for i in range(len(data), 0, -1 * chunkstep):
        if i - chunklength > 0:
            slicestart = i - chunkstep
            sliceend = i
            seismo_data = data[slicestart:sliceend]
            utctimes = utcobj[slicestart:sliceend]
            returnlist = [utctimes, seismo_data, sliceend, ddminmax]
            yield returnlist
        else:
            yield None


def main(utcobj, data):
    # Set up for multiprocessing
    chunklength = 60 * 60 * 10
    # The next step we're picking the data off from. (Every 5 mins usually)
    chunkstep = 60 * 60 * 10

    sz_avg = np.nanmean(data)
    # # Use the RMS for the margin
    # margin = np.sqrt(np.mean(np.square(data))) * 4
    margin = np.std(data) * 8
    ddminmax = [sz_avg - margin, sz_avg + margin]

    # dx_avg = np.nanmean(dxdt)
    # # # Use the RMS for the margin
    # # margin = np.sqrt(np.mean(np.square(dxdt))) * 0.5
    # margin = np.std(dxdt) * 0.5
    # dxminmax = [dx_avg - margin, dx_avg + margin]

    cores = cpu_count() - 1
    with ProcessPoolExecutor(max_workers=cores) as executor:
        results = list(
            executor.map(
                process_chunk,
                chunks(utcobj, data, chunkstep, chunklength, ddminmax)
                )
            )
        # print(f'{results}')
