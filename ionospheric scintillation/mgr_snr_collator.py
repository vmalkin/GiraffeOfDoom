from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from datetime import datetime
from time import time
from statistics import mean, median
from numpy import nan
import os

utc_format = '%d %H:%M'
working_dir = "images"
epoch_now = int(time())
epoch_start = int(epoch_now - 86400)
binsize = 60
satellite_index_size = 201


def get_index(posixtime):
    # div = (epoch_now - epoch_start) / binsize
    indexvalue = (posixtime - epoch_start) / binsize
    indexvalue = round(indexvalue, 0)
    indexvalue = int(indexvalue)
    return indexvalue


def posix2utc(posixtime):
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(utc_format)
    return utctime


def create_chart(x_data, y_data):
    try:
        name = "snr.jpg"
        x = x_data
        y1 = y_data

        # for data in snrdata:
        #     x.append(data[0])
        #     y1.append(data[1])
        # print(y1)

        snr, ax = plt.subplots(figsize=[12,4], dpi=100)
        tic_major = 60
        tic_minor = 15
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_major))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(tic_minor))

        ax.tick_params(axis='x', labelrotation=90)
        # ax.set_ylim(0, 50)
        ax.grid(True, which='major', color="#ccb3b3")
        ax.grid(True, which='minor', color="#e0e0e0")

        ax.set_xlabel("Time UTC")
        ax.set_ylabel("S/N Ratio - dB")

        plt.plot(x, y1, color="black", linewidth=1)
        # plt.rcParams.update({'font.size': 6})
        filepath = working_dir + "//" + name
        snr.tight_layout()
        plt.savefig(filepath)
    except:
        print("Unable to save image file")
    plt.close('all')

def satellite_index_generator():
    """Generate hash table for satellite names """
    sid1 = 'gps_'
    sid2 = 'glonass_'
    indices = {}
    for i in range(0, satellite_index_size):
        name = sid1 + str(i)
        indices[name] = i

    for i in range(0, satellite_index_size):
        step = satellite_index_size
        name = sid2 + str(i)
        indices[name] = i + step
    print("Length of satellite hash table is " + str(len(indices)) + " records")
    return indices

# query results format:
# sat_id, posixtime, alt, az, s4, snr
def wrapper(queryresults):
    datearray = []
    t = epoch_start
    for i in range(0, 1442):
        t = t + binsize
        datearray.append(posix2utc(t))

    dataarray = []
    for i in range(0, 1442):
        dataarray.append(nan)

    satelliteindex = satellite_index_generator()
    satelite_list = []
    for i in range(0, (satellite_index_size * 2 + 1)):
        satelite_list.append(dataarray)

    for line in queryresults:
        satid = satelliteindex[line[0]]
        dataid = get_index(line[1])
        satelite_list[satid][dataid] = line[5]


    for line in satelite_list:
        print(line[1])










