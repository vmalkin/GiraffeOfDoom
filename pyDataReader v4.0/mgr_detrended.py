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
    index_a = None
    index_b = None
    data_a = None
    data_b = None

    for i in range(0, len(datalist)):
        if datalist[i].timevalue == startposix:
            index_a = i
            data_a = datalist[i].base_value
        if datalist[i].timevalue == endposix:
            index_b = i
            data_b = datalist[i].base_value
    index_step = index_b - index_a
    data_step = data_b - data_a
    data_bits = data_step / index_step

    for j in range(index_a, index_b):
        prev = datalist[j].base_value
        datalist[j].smooth_value = prev + data_bits
    return datalist


def calc_middle(datalist, windowstart):
    # determine how many records constitute the half window value
    windowindex = None
    for i in range(0, len(datalist)):
        if datalist[i].timevalue > windowstart:
            windowindex = i
        # we dont need to iterate thru any more of the loop
        break

    for j in range(windowindex, len(datalist) - windowindex):
        temp=[]
        for k in range(-1 * windowindex, windowindex):
            value = float(datalist[k + j].base_value)
            temp.append(value)
        avg = mean(temp)
        datalist[j].smooth_value = avg
    return datalist



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
