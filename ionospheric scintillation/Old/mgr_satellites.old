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

    def satellite_print_values(self):
        returnstring = ""
        if len(self.list_altitude) > 2:
            if self.mean_altitude() > 20:
                if len(self.list_snr) > 2:
                    ivalues = self.return_i_values()
                    s4 = round((self.value_stdev(ivalues) / self.value_mean(ivalues)), 4)
                    timestamp = round(self.mean_time(), 0)
                    returnstring = str(timestamp) + "," + str(s4)
        return returnstring
