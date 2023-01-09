from statistics import mean

import standard_stuff
from standard_stuff import posix2utc
from plotly import graph_objects as go

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


def plot(dt_dates, dt_detrend, savefile_name):
    plotdata = go.Scatter(x=dt_dates, y=dt_detrend, mode="lines")
    fig = go.Figure(plotdata)
    fig.show()


def wrapper(datalist, publishdirector):
    # If the length of the datalist is long enough, attempt to use the full algorthm,
    # Otherwise use a simple linear approximation

    # THE DATALIST IS IN THE FORMAT "posixtime, data" We will need to split this into two lists
    # Dates and actual data.
    savefile_name = publishdirector + "//" + "current_detrended.csv"

    dt_dates = []
    dt_data = []
    for item in datalist:
        utcdate = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M')
        dt_dates.append(utcdate)
        dt_data.append(item[1])


    if len(dt_data) < half_window:
        f = calc_start(dt_data)
    else:
        # Calculate the detrended data.
        a = calc_start(dt_data)
        b = calc_middle(dt_data)
        c = calc_end(dt_data)
        f = a + b + c

    # Generate residuals, thus flattening out the original data. dt_detrend
    # is the final detrended data.
    dt_detrend = []
    for i in range(0, len(f)):
        dd = float(dt_data[i])
        ff = float(f[i])
        d = round((dd - ff), 3)
        dt_detrend.append(d)
    try:
        print("*** Detrended Magnetogram: Created")
        plot(dt_dates, dt_detrend, savefile_name)
    except:
        print("!!! Detrended Magnetogram: FAILED to plot magnetogram")

