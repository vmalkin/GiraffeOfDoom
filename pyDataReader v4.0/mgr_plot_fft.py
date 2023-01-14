from statistics import mean
import standard_stuff
import os
import sqlite3
from time import time
from plotly import graph_objects as go
import numpy as np
import constants as k

# The number of readings that equates to one and a half hours of time.
half_window = 10


def plot(dt_detrend, savefile_name):
    width = k.plot_width
    height = k.plot_height
    backgroundcolour = k.plot_backgroundcolour
    pencolour = k.plot_pencolour
    gridcolour = k.plot_gridcolour

    title = "Geomagnetic Field: Horizontal Component with Diurnal Variation. "
    title = title +  "<i>Updated " + standard_stuff.posix2utc(time(), '%Y-%m-%d %H:%M') + "</i>"

    plotdata = go.Scatter(y=dt_detrend, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br>http://RuruObservatory.org.nz",
                      yaxis_title="Frequency")
    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_layout(showlegend=False,
                      font_family="Courier New")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                     zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
    fig.update_xaxes(nticks=12, ticks='outside',
                     tickformat="%b %d<br>%H:%M")
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



def wrapper(dd, publishdirectory):
    print("*** Fast Fourier: START")
    # THE DATALIST IS IN THE FORMAT "posixtime, data" We will need to split this into two lists
    # Dates and actual data.
    datalist = database_get_data(dd)
    t = []
    for item in datalist:
        t.append(item[1])
    fourier = np.fft.fft(t)
    for item in fourier:
        print(item)

    # try:
    # savefile_name = publishdirectory + os.sep + "plot_fft.jpg"
    # plot(fourier, savefile_name)
    # print("*** Fast Fourier: END")
    # except:
    #     print("!!! Fast Fourier: FAILED to plot fft")

