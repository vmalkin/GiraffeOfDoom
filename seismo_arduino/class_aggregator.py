import numpy as np
from numpy import mean, median
import constants as k


class Aggregator:
    def __init__(self, posixstart, posixstop):
        self.data_null = np.nan
        self.date_start = posixstart  # should be POSIX values
        self.date_stop = posixstop  # should be POSIX values
        self.data_seismo = []
        self.data_temperature = []
        self.data_pressure = []

    def get_data_avg(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        val_avg = self.data_null
        if len(dataset) > 0:
            try:
                val_avg = round(np.nanmean(dataset), 4)
            except RuntimeWarning:
                pass
        return val_avg

    def get_data_median(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        if len(dataset) > 0:
            val_median = round(np.nanmedian(dataset), 4)
        else:
            val_median = self.data_null
        return val_median

    def get_data_max(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        if len(dataset) > 0:
            val_max = round(np.nanmax(dataset), 4)
        else:
            val_max = self.data_null
        return val_max

    def get_data_min(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        if len(dataset) > 0:
            val_min = round(np.nanmin(dataset), 4)
        else:
            val_min = self.data_null
        return val_min

    def get_reading_posix(self):
        # avg_time = round((self.date_start + self.date_stop) / 2, 4)
        # return avg_time
        return self.date_stop

# This function performs aggregation using the Aggregator class
# querydata has the format [posix, seismo, temp, pressure]
def aggregate_data(windowsize, querydata):
    # windowsize needs to be at least 1
    # PASS 1 - Set up the array
    print("PASS 1 - Setting up aggregating array")
    aggregate_array = []
    date_start = 0
    for i in range(0, len(querydata), windowsize):
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
        if i % windowsize == 0:
            j = j + 1


    # PASS 3 - add the data into the correct aggregate object based on datetime
    print("PASS 3 - Adding data to aggregating array")
    for i in range(0, len(querydata)):
        # if i % 1000 == 0:
        #     print(f"{i} / {len(result_7d)}")
        datetime = querydata[i][0]
        seismo = float(querydata[i][1])
        temp = float(querydata[i][2])
        pressure = float(querydata[i][3])
        agg_index = lookup[datetime]
        aggregate_array[agg_index - 1].data_seismo.append(seismo)
        aggregate_array[agg_index - 1].data_temperature.append(temp)
        aggregate_array[agg_index - 1].data_pressure.append(pressure)


    # # PASS 4 - Use aggregator class functions to create plotting data
    # print("PASS 4 - Create and return plotting array [posixdatetime, avg_seismo, avg_temp, avg_pressr]")
    # plotting_data = []
    # for i in range(1, len(aggregate_array)):
    #     tim = aggregate_array[i].get_avg_posix()
    #     siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
    #     tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
    #     prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
    #     d = [tim, siz, tmp, prs]
    #     plotting_data.append(d)

    # return plotting_data
    return aggregate_array