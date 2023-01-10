from statistics import mean
import standard_stuff
import os
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
    width = 1500
    height = 500
    backgroundcolour = "#ffffff"
    pencolour = "#600000"
    gridcolour = "#909090"

    plotdata = go.Scatter(x=dt_dates, y=dt_detrend, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title="H-Component",
                      xaxis_title="Date/time UTC<br><sub>http://RuruObservatory.org.nz</sub>",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")
    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)

    fig.write_image(savefile_name)


def wrapper(datalist, publishdirectory):
    # If the length of the datalist is long enough, attempt to use the full algorthm,
    # Otherwise use a simple linear approximation

    # THE DATALIST IS IN THE FORMAT "posixtime, data" We will need to split this into two lists
    # Dates and actual data.
    savefile_name = publishdirectory + os.sep + "plot_diurnal.jpg"
    dt_dates = []
    dt_data = []
    for item in datalist:
        utcdate = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
        dt_dates.append(utcdate)
        dt_data.append(float(item[1]))

    # ########## Filtering and Adjustment before Plotting ##########
    # Smooth the data before plotting
    dt_data = standard_stuff.filter_median(dt_data, 2)
    dt_data = standard_stuff.filter_mean(dt_data, 250)

    # the datetimes will be of a different length now because of the filtering of the data
    # Determin the difference and top and tail the datetimes array.
    toptail = len(dt_dates) - len(dt_data)
    dt_dates = dt_dates[toptail:-toptail]
    # ########## Filtering and Adjustment before Plotting ##########

    try:
        print("*** Diurnal Magnetogram: Created")
        plot(dt_dates, dt_data, savefile_name)
    except:
        print("!!! Diurnal Magnetogram: FAILED to plot magnetogram")

