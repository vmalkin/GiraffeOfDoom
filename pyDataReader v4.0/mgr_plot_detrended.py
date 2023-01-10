import os
from time import time
from statistics import mean
import standard_stuff
import sqlite3
from plotly import graph_objects as go

# The number of readings that equates to one and a half hours of time.
half_window = int(60 * 60 * 1.5)

def calc_start(datalist):
    returnlist = []
    data_start = datalist[0]
    data_end = datalist[half_window - 1]
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
    data_start = datalist[len(datalist) - half_window]
    data_end = datalist[len(datalist) - 1]
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
    fig.update_layout(width=width, height=height, title="H-Component - Detrended",
                      xaxis_title="Date/time UTC<br><sub>http://RuruObservatory.org.nz</sub>",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")
    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)

    fig.write_image(savefile_name)


def getposixtime():
    timevalue = int(time())
    return timevalue


def database_get_data(dba):
    tempdata = []
    starttime = getposixtime() - 86400
    db = sqlite3.connect(dba)
    try:
        cursor = db.cursor()
        result = cursor.execute("select * from data where data.posixtime > ? order by data.posixtime asc", [starttime])
        for line in result:
            dt = line[0]
            da = line[1]
            d = [dt, da]
            tempdata.append(d)

    except sqlite3.OperationalError:
        print("Database is locked, try again!")
    db.close()
    return tempdata

def wrapper(database, publishdirectory):
    processdata = database_get_data(database)
    # If the length of the datalist is long enough, attempt to use the full algorthm,
    # Otherwise use a simple linear approximation

    # THE DATALIST IS IN THE FORMAT "posixtime, data" We will need to split this into two lists
    # Dates and actual data.
    savefile_name = publishdirectory + os.sep + "plot_detrended.jpg"
    dt_dates = []
    dt_data = []
    for item in processdata:
        utcdate = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
        dt_dates.append(utcdate)
        dt_data.append(float(item[1]))


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

    # ########## Filtering and Adjustment before Plotting ##########
    # Smooth the data before plotting
    dt_detrend = standard_stuff.filter_median(dt_detrend, 2)
    dt_detrend = standard_stuff.filter_mean(dt_detrend, 250)

    # the datetimes will be of a different length now because of the filtering of the data
    # Determin the difference and top and tail the datetimes array.
    toptail = len(dt_dates) - len(dt_detrend)
    dt_dates = dt_dates[toptail:-toptail]
    # ########## Filtering and Adjustment before Plotting ##########

    try:
        print("*** Detrended Magnetogram: Created")
        plot(dt_dates, dt_detrend, savefile_name)
    except:
        print("!!! Detrended Magnetogram: FAILED to plot magnetogram")

