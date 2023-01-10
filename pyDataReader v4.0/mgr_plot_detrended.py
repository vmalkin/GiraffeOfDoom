import os
from time import time
from statistics import mean, median
import standard_stuff
import sqlite3
from plotly import graph_objects as go

class DataPoint:
    def __init__(self):
        self.posixtime = 0
        self.data_raw = 0
        self.data_medianed = 0
        self.data_avg = 0

def plot(dates, data1, data2, savefile_name):
    width = 1500
    height = 500
    backgroundcolour = "#ffffff"
    pencolour = "#600000"
    gridcolour = "#909090"

    plotdata = go.Scatter(x=dates, y=data1, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title="H-Component - Detrended",
                      xaxis_title="Date/time UTC<br><sub>http://RuruObservatory.org.nz</sub>",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")

    if data2 is not None:
        fig.add_scatter(x=dates, y=data2, mode="lines", connectgaps=True,
                        line=dict(color="#002050", width=3))

    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)

    fig.write_image(savefile_name)


def getposixtime():
    timevalue = int(time())
    return timevalue


def database_get_data(dba):
    tempdata = []
    # Grab a bit more than a day so we can do the running average with a bit of lead data
    starttime = getposixtime() - 91800
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
    print("*** Detrended: START")
    readings = database_get_data(database)

    # Create datapont array
    array_datapoints = []
    for item in readings:
        d = DataPoint()
        d.posixtime = item[0]
        d.data_raw = item[1]
        array_datapoints.append(d)

    # find median value for each datapoint
    halfwindow_median = 3
    for i in range(halfwindow_median, len(array_datapoints) - halfwindow_median):
        t = []
        for j in range(-halfwindow_median, halfwindow_median):
            t.append(array_datapoints[i + j].data_raw)
        x = median(t)
        array_datapoints[i].data_medianed = x

    # Calculate the running average using a 3 hour window
    halfwindow_average = int(30 * 60 * 1.5)
    t = []
    for i in range(0, len(array_datapoints)):
        t.append(array_datapoints[i].data_medianed)
        if len(t) >= 2 * halfwindow_average:
            array_datapoints[i - halfwindow_average].data_avg = mean(t)
            t.pop(0)

    # Calculate the 3 hour running average
    d_time = []
    d_median = []
    d_average = []
    for d in array_datapoints:
        tt = standard_stuff.posix2utc(d.posixtime, '%Y-%m-%d %H:%M:%S')
        d_time.append(tt)
        if d.data_medianed is 0:
            d_median.append(None)
        else:
            d_median.append(d.data_medianed)

    savefile = publishdirectory + os.sep + "test.jpg"
    plot(d_time, d_median, None, savefile)
    print("*** Detrended: FINISHED")