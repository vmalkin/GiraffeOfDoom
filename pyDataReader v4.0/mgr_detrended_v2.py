from statistics import mean

# The number of readings that equates to one and a half hours of time.
half_window = 10

def calc_start(datalist):
    returnlist = []
    data_start = float(datalist[0])
    data_end = float(datalist[half_window - 1])
    rate = (data_end - data_start) / half_window
    d = data_start
    returnlist.append(data_start)

    for i in range(0, half_window - 1):
        d = d + rate
        returnlist.append(round(d,3))
        # print(i, datalist[i], returnlist[i])
    return returnlist


def calc_end(datalist):
    returnlist = []
    data_start = float(datalist[len(datalist) - half_window])
    data_end = float(datalist[len(datalist) - 1])
    rate = (data_end - data_start) / half_window
    d = data_start
    returnlist.append(data_start)

    for i in range(len(datalist) - half_window, len(datalist) - 1):
        d = d + rate
        returnlist.append(round(d,3))
    return returnlist


def calc_middle(datalist):
    returnlist = []

    for i in range(half_window, len(datalist) - half_window):
        t = []
        for j in range(0 - half_window, half_window):
            t.append(float(datalist[i + j]))

        if len(t) > 0:
            d = mean(t)
        else:
            d = 0
        returnlist.append(round(d,3))

    return returnlist


def parse_dates(datalist):
    pass


def wrapper(datalist):
    # If the length of the datalist is long enough, attempt to use the full algorthm,
    # Otherwise use a simple linear approximation

    if len(datalist) < half_window:
        f = calc_start(datalist)
    else:
        # Calculate the detrended data.
        a = calc_start(datalist)
        b = calc_middle(datalist)
        c = calc_end(datalist)
        f = a + b + c

    # Generate residuals, thus flattening out the original data. T is the final detrended data.
    t = []
    for i in range(0, len(f)):
        d = round((datalist[i] - f[i]), 3)
        t.append(d)
    return t
