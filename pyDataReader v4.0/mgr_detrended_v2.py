from statistics import mean

# The number of readings that equates to one and a half hours of time.
half_window = 5

def calc_start(datalist):
    returnlist = []
    data_start = datalist[0]
    data_end = datalist[half_window - 1]
    rate = (data_end - data_start) / half_window
    d = data_start

    for i in range(0, half_window):
        d = d + rate
        returnlist.append(round(d,3))
    return returnlist


def calc_end(datalist):
    returnlist = []
    data_start = datalist[len(datalist) - half_window]
    data_end = datalist[len(datalist) - 1]

    rate = (data_end - data_start) / half_window
    d = data_start
    for i in range(0, half_window):
        d = d + rate
        returnlist.append(round(d,3))
    return returnlist


def calc_middle(datalist):
    returnlist = []

    for i in range(half_window + 1, len(datalist) - half_window):
        t = []
        for j in range(0 - half_window, half_window):
            t.append(datalist[i + j])

        if len(t) > 0:
            d = mean(t)
        else:
            d = 0
        returnlist.append(round(d,3))
        t = []
    return returnlist


def parse_dates(datalist):
    pass


def wrapper(datalist, publishdir):
    pass
