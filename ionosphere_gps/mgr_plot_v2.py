import time
import secrets
from plotly import graph_objects as go
import datetime
from statistics import mean, stdev, median
import standard_stuff

# one and a half hours is 2700 lots of 2 seconds
readings_per_minute = 60
avg_half_window = int(readings_per_minute * 5)
median_half_window = int(readings_per_minute * 2)


class Day:
    def __init__(self):
        self.lat = self.create_datastore()
        self.long = self.create_datastore()
        self.alt = self.create_datastore()
        self.hdop = self.create_datastore()

    def create_datastore(self):
        t = []
        for i in range(0, 1440):
            t.append([])
        return t

    def report_length(self, array):
        length = len(array)
        print("Length is: ", length)


def wrapper(db_data, label):
    print("*** Plotter starting...")
    # ['1683423236', '4552.29376', '17029.07', '2', '10', '1.06', '196.4']
    # posixtime, lat, long, position_fix, num_sats, hdop, alt
    # Indices of data
    psxtime = 0
    lat = 1
    long = 2
    numsats = 4
    hdop = 6
    alt = 6
    current_day = None

    day_stack = []
    for gpsdata in db_data:
        index_day = standard_stuff.posix2utc(gpsdata[psxtime], "%d")
        if index_day != current_day:
            current_day = index_day
            d = Day()
        index_minute = int(standard_stuff.posix2utc(gpsdata[psxtime], "%M"))
        d.lat[index_minute].append(gpsdata[lat])
        d.long[index_minute].append(gpsdata[long])
        d.alt[index_minute].append(gpsdata[alt])
        d.hdop[index_minute].append(gpsdata[hdop])
    #     index_hour = standard_stuff.posix2utc(gpsdata[posixtime], "%H")
    #     index_minute = standard_stuff.posix2utc(gpsdata[posixtime], "%M")
    for day in day_stack:
        day.report_length(day.lat)


