import datetime

class DP_processed():
    def __init__(self):
        self.posix_time = 0
        self.data = 0
        self.sr = 0

    def calculate_residual(self):
        residual = self.data - self.sr
        return residual

    def posix2utc(self, posixvalue):
        utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        return utctime

    def print_values_utc(self):
        returnstring = str(self.posix2utc(self.posix_time)) + "," + str(self.calculate_residual())
        return returnstring

def processor_sr1(data_array):
    """
    This function takes an array of readings in [posix_time, data] format and calculate Sr - the diurnal curve.
    It returns an array that
    :return:
    """
    returnarray = []
    return returnarray


def processor_wrapperfunction(data_array):
    if len(data_array) > 90:
        returnarray=[]
    else:
        returnarray = data_array

