import datetime
from statistics import mean

class Datapoint:
    def __init__(self, value=0, time=""):
        self.base_value = value
        self.smooth_value = 0
        self.timevalue = time

    def _return_residual(self):
        r = self.base_value - self.smooth_value
        return r


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime



def calc_ends(datalist, startposix, endposix):
    pass


def calc_middle(datalist, windowstart, windowend, halfwindow):
    temp = []
    for i in range(0, len(datalist)):
        temp.append(datalist[i].base_value)


# data is in the format [posixtime, value]
def wrapper(data, publishdir):
    halfwindow = 5400
    # create a list of datapoints
    datalist = []
    for item in data:
        i = item.strip()
        i = item.split(",")
        d = Datapoint(i[1], i[0])
        datalist.append(d)

    time_start = int(datalist[0].timevalue)
    time_end = int(datalist[len(datalist) - 1].timevalue)

    # if the elapsed time is 6 hours, start calculations
    if (time_end - time_start) > 21600:
        t_windowstart = time_start + halfwindow
        t_windowend = time_end - halfwindow

        datalist = calc_ends(datalist, time_start, t_windowstart )
        datalist = calc_ends(datalist, t_windowend, time_end)
        datalist = calc_middle(datalist)



    # we need to create a symmetrical running average with a 3 hour window
    # we will use a simple linear approximation for the 1.5 hour ends of the list of data.
