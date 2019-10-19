import math
from statistics import mean, stdev


class Satellite:
    def __init__(self):
        self.list_posix = []
        self.list_snr = []
        self.list_altitude = []
        self.list_azimuth = []

    def return_i_values(self):
        returnlist = []
        for value in self.list_snr:
            ivalue = math.pow(10, (value/10))
            returnlist.append(ivalue)
        return returnlist

    def value_stdev(self, valuelist):
        stdev_value = stdev(valuelist)
        return stdev_value

    def value_mean(self, valuelist):
        mean_value = mean(valuelist)
        return mean_value

    def mean_altitude(self):
        mean_value = mean(self.list_altitude)
        return mean_value

    def mean_azimuth(self):
        mean_value = mean(self.list_azimuth)
        return mean_value

    def mean_time(self):
        mean_value = mean(self.list_posix)
        return mean_value