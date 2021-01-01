from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from numpy import NaN
from datetime import datetime
from time import time
epoch_now = int(time())
epoch_start = epoch_now - (60* 60 * 24)
binsize = 60
constellation_count = 200

class Satellite:
    def __init__(self, name):
        self.name = name
        self.data = self.create_datastore()
        self.

    def create_datastore(self):
        d = []
        for i in range(0, 1441):
            d.append(NaN)
        return d


def posix2utc(posixtime):
    timeformat = '%d  %H:%M'
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def get_index(currentposix):
    # div = (epoch_now - epoch_start) / binsize
    indexvalue = (currentposix - epoch_start) / 60
    indexvalue = int(round(indexvalue, 0))
    return indexvalue

def create_satellite_dictionary():
    """Creates a lookup table so when we supply the satellite name and number, we get a unique index value."""
    s = {}
    constellation = "gps_"
    for i in range (0, constellation_count + 1):
        key = constellation + str(i)
        value = i
        s[key] = value

    constellation = "glonass_"
    for i in range (1, constellation_count + 1):
        j = constellation_count + i
        key = constellation + str(i)
        value = j
        s[key] = value
    return s


def parse_query_to_satellite(queryresults):
    pass


def create_snr_chart(satellites, times):
    name = "test.jpg"
    snr, ax = plt.subplots(figsize=[12, 4], dpi=100)
    tic_major = 60
    tic_minor = 15
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_major))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(tic_minor))

    ax.tick_params(axis='x', labelrotation=90)
    ax.set_ylim(0, 100)
    ax.grid(True, which='major', color="#ccb3b3")
    ax.grid(True, which='minor', color="#e0e0e0")

    ax.set_xlabel("Time UTC")
    ax.set_ylabel("S/N Ratio")

    for s in satellites:
        r = []
        for dp in s.data:
            r.append(dp)
        # print(r)
        plt.plot(times, r, color="blue", linewidth=1, alpha=0.4)

    plt.rcParams.update({'font.size': 6})
    plt.savefig(name)
    plt.close('all')


def create_timestamps():
    ts = []
    for i in range(epoch_start - binsize, epoch_now, binsize):
        ts.append(posix2utc(i))
    return ts

def create_constellation():
    c = []
    for i in range(0, constellation_count*2):
        c.append(Satellite(i))
    return c

# query results format:
# sat_id, posixtime, alt, az, s4, snr
def wrapper(queryresults):
    timestamps = create_timestamps()
    satellite_dictionary = create_satellite_dictionary()
    constellation = create_constellation()

    for entry in queryresults:
        if entry[2] >= 40:
            satellite_name = satellite_dictionary[entry[0]]
            if satellite_name <= (2*constellation_count):
                data_index = get_index(entry[1])
                if data_index <= 1440:
                    datavalue = entry[4]
                    constellation[satellite_name].data[data_index] = datavalue

    create_snr_chart(constellation, timestamps)
