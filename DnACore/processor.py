import datetime
import constants as k

class DP_processed():
    def __init__(self, posixtime, datavalue):
        self.posix_time = posixtime
        self.data = datavalue
        self.sr = k.null_output_value

    def calculate_residual(self):
        residual = self.data - self.sr
        return residual

    def posix2utc(self, posixvalue):
        utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        return utctime


def processor_dvdt(data_array):
    """
    This function takes an array of readings in [posix_time, data] format and calculate simple dv/dt,
    with a smoothed curve on a 10min window
    :return:
    """
    returnarray = []
    for i in range(1, len(data_array)):
        dvdt = data_array[i].data - data_array[i-1].data
        datetime = data_array[i].posix_time
        dp = DP_processed(datetime, dvdt)
        returnarray.append(dp)
    return returnarray

def processor_smooth(datarray):
    returnarray = []



def processor_wrapperfunction(data_array):
    if len(data_array) > 90:
        returnarray=[]
    else:
        returnarray = data_array

