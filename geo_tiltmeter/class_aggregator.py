import numpy as np
# from numpy import mean, median
# import constants as k
from datetime import datetime, timezone


class Aggregator:
    def __init__(self, posixstart, posixstop):
        # self.data_null = np.nan
        self.data_null = 9999
        self.date_start = posixstart  # should be POSIX values
        self.date_stop = posixstop  # should be POSIX values
        self.data_seismo = []
        # self.data_temperature = []
        # self.data_pressure = []

    def get_data_avg(self, dataset):    # return the median value of the data set. If the set is empty, return a null
        if len(dataset) > 0:
            val_avg = round(np.mean(dataset), 4)
            return val_avg
        else:
            return 9999

    def get_avg_posix(self):
        avg_time = round((self.date_start + self.date_stop) / 2, 4)
        return avg_time

    def return_utc_timeobject(self, psx):
        tim = datetime.fromtimestamp(psx, tz=timezone.utc)
        return tim

# This function performs aggregation using the Aggregator class
# querydata has the format [posix, seismo]
def aggregate_data(windowsize, querydata):
    # windowsize needs to be at least 1
    # PASS 1 - Set up the array
    print("PASS 1 - Setting up aggregating array")
    aggregate_array = []
    date_start = querydata[0][0]
    for i in range(1, len(querydata), windowsize):
        date_end = querydata[i][0]
        d = Aggregator(date_start, date_end)
        aggregate_array.append(d)
        date_start = date_end

    # PASS 2 - generate the lookup array to speed up data placement
    print("PASS 2 - Generating lookup dict")
    lookup = {}
    j = 0
    for i in range(0, len(querydata)):
        key = (querydata[i][0])
        value = (j)
        lookup[key] = value
        # the key value is the position of the aggregate object in the aggregate array.
        # the windowsize is what clicks-over to indicate when an item from the query data has a date range that
        # should go into the next aggregate object
        if i % windowsize == 0:
            j = j + 1

    # PASS 3 - add the data into the correct aggregate object based on datetime
    print("PASS 3 - Adding data to aggregating array")
    for i in range(0, len(querydata)):
        # if i % 1000 == 0:
        #     print(f"{i} / {len(result_7d)}")
        datetime = querydata[i][0]
        seismo = querydata[i][1]
        agg_index = lookup[datetime]
        aggregate_array[agg_index - 1].data_seismo.append(seismo)

    # PASS 4 - Use aggregator class functions to create plotting data
    print("PASS 4 - Create and return plotting array.")
    utc_object_time = []
    seismic_data = []
    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = aggregate_array[i].return_utc_timeobject(tim)
        siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
        utc_object_time.append(tim)
        seismic_data.append(siz)

    # return plotting_data
    return [utc_object_time, seismic_data]