import datetime
from statistics import mean

class Datapoint:
    def __init__(self, value=0, time=""):
        self.base_value = value
        self.smooth_value = 0
        self.timevalue = time

    def return_residual(self):
        r = float(self.base_value) - float(self.smooth_value)
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


def calc_middle(datalist, hw_time):
    # determine how many records constitute the half window value
    windowindex = 0
    for i in range(0, len(datalist)):
        if int(datalist[i].timevalue) > int(hw_time):
            windowindex = i
            # we dont need to iterate thru any more of the loop
            break

    # Calculate the running average for the middle of the data
    for i in range(windowindex, len(datalist) - windowindex):
        temp = []
        for j in range(0-windowindex, windowindex):
            temp.append(float(datalist[i + j].base_value))
        avg = mean(temp)
        datalist[i].smooth_value = avg
        temp=[]

    # calculate the simple linear approximation for the start
    a = float(datalist[0].base_value)
    b = float(datalist[windowindex].base_value)
    diff = (b - a) / windowindex
    datalist[0].smooth_value = datalist[0].base_value
    for i in range(1, windowindex):
        datalist[i].smooth_value = float(datalist[i-1].smooth_value) + diff

    # calculate the simple linear approximation for the end
    end_start_index = len(datalist) - windowindex
    end_end_index = len(datalist) - 1
    a = float(datalist[end_start_index].base_value)
    b = float(datalist[end_end_index].base_value)
    diff = (b - a) / windowindex

    datalist[windowindex].smooth_value = datalist[windowindex].base_value
    for i in range(end_start_index, len(datalist) - 1):
        datalist[i].smooth_value = float(datalist[i-1].smooth_value) + diff


# data is in the format [posixtime, value]
def wrapper(data, publishdir):
    halfwindow = 5400  # in seconds
    # create a list of datapoints

    datalist = []
    for item in data:
        a = item.split("\n")
        b = a[0]
        i = b.split(",")
        d = Datapoint(i[1], i[0])
        datalist.append(d)

    time_start = int(datalist[0].timevalue)
    time_end = int(datalist[len(datalist) - 1].timevalue)

    # if the elapsed time is 6 hours, start calculations
    if (time_end - time_start) > 21600:
        hw_time = time_start + halfwindow
        calc_middle(datalist, hw_time)

    datalist.pop(len(datalist) - 1)

    savefile = publishdir + "/detrended.csv"

    with open(savefile, "w") as s:
        s.write("UTC date, base value, average, detrended value\n")
        for dp in datalist:
            timestring = posix2utc(dp.timevalue,'%Y-%m-%d %H:%M:%S')
            d = str(timestring + "," + str(dp.base_value) + "," + str(dp.smooth_value) + "," + str(dp.return_residual()))
            s.write(d + "\n")
