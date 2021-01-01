from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from numpy import NaN
from datetime import datetime
from time import time
epoch_now = int(time())
epoch_start = epoch_now - (60* 60 * 24)
binsize = 60
constellation_count = 300

class Satellite:
    def __init__(self):
        # self.name = name
        self.data = self.create_datastore()

    def create_datastore(self):
        d = []
        for i in range(0, 1441):
            d.append([NaN])
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


def create_snr_chart():
    pass


def create_timestamps():
    ts = []
    for i in range(epoch_start, epoch_now, binsize):
        ts.append(posix2utc(i))
    return ts

def create_constellation():
    c = []
    for i in range(0, constellation_count*2):
        c.append(Satellite)
    return c

# query results format:
# sat_id, posixtime, alt, az, s4, snr
def wrapper(queryresults):
    timestamps = create_timestamps()
    satellite_dictionary = create_satellite_dictionary()
    constellation = create_constellation()

    for entry in queryresults:
        print(entry[0])


    # parse_query_to_satellite(queryresults)
    # create_snr_chart()
