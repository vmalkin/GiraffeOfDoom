import os
from time import time
from statistics import mean, median
import standard_stuff
import sqlite3
from plotly import graph_objects as go
import constants as k

null_value = f'null'
# make this the median reading for 60 seconds worth of data
halfwindow_median = 5
# readings per minute x 60 mins x 1.5 hours
halfwindow_average = int(60 * 60 * 1.5)
# halfwindow_average = 300


class DataPoint:
    def __init__(self):
        self.posixtime = 0
        self.data_raw = 0
        self.data_medianed = 0
        self.data_3hr_avg = 0
        self.residual = 0

def plot(dates, data1, data2, title, savefile_name):
    width = k.plot_width
    height = k.plot_height
    backgroundcolour = k.plot_backgroundcolour
    pencolour = k.plot_pencolour
    gridcolour = k.plot_gridcolour
    title = title +  "<i>Updated " + standard_stuff.posix2utc(time(), '%Y-%m-%d %H:%M') + "</i>"

    plotdata = go.Scatter(x=dates, y=data1, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br>http://RuruObservatory.org.nz",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")

    if data2 is not None:
        fig.add_scatter(x=dates, y=data2, mode="lines", connectgaps=False,
                        line=dict(color="#0080f0", width=3))

    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_layout(showlegend=False,
                      font_family="Courier New")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                     zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
    fig.update_xaxes(nticks=12, ticks='outside',
                     tickformat="%b %d<br>%H:%M")
    fig.write_image(savefile_name)


def plot_kindex(k_plotdates, k_plotvalues, title, savefile):
    width = k.plot_width
    height = k.plot_height
    backgroundcolour = k.plot_backgroundcolour
    pencolour = k.plot_pencolour
    gridcolour = k.plot_gridcolour
    title = title + "<i>Updated " + standard_stuff.posix2utc(time(), '%Y-%m-%d %H:%M') + "</i>"

    plotdata = go.Bar(x=k_plotdates, y=k_plotvalues, marker_color=pencolour)
    fig = go.Figure(plotdata)

    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br>http://RuruObservatory.org.nz",
                      yaxis_title="Activity Index")

    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_layout(showlegend=False,
                      font_family="Courier New")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                     zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
    # fig.update_xaxes(nticks=12, ticks='outside',
    #                  tickformat="%b %d<br>%H:%M")
    fig.write_image(savefile)

def getposixtime():
    timevalue = int(time())
    return timevalue


def database_get_data(dba, starttime):
    tempdata = []
    # Grab a bit more than a day so we can do the running average with a bit of lead data
    # starttime = getposixtime() - 91800
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


def remove_zeros(inputarray):
    outputarray = []
    for item in inputarray:
        if item == 0:
            outputarray.append(null_value)
        else:
            outputarray.append(item)
    return outputarray


def wrapper(data, publishdirectory):
    readings = data

    if len(readings) > halfwindow_average * 2:
        # Create datapont array
        array_datapoints = []
        for item in readings:
            d = DataPoint()
            d.posixtime = item[0]
            d.data_raw = item[1]
            array_datapoints.append(d)

        # find median value for each datapoint
        t = []
        for i in range(0, len(array_datapoints)):
            t.append(array_datapoints[i].data_raw)
            if len(t) >= 2 * halfwindow_median:
                array_datapoints[i - halfwindow_median].data_medianed = median(t)
                t.pop(0)

        # Calculate the running average using a 3-hour window
        t = []
        for i in range(0, len(array_datapoints) - 1):
            t.append(array_datapoints[i].data_medianed)
            if len(t) >= 2 * halfwindow_average:
                array_datapoints[i - halfwindow_average + 1].data_3hr_avg = mean(t)
                t.pop(0)

        # # Calculate the running average using a 3-hour window
        # for i in range(halfwindow_average, len(array_datapoints) - halfwindow_average):
        #     t = []
        #     for j in range(-halfwindow_average, halfwindow_average):
        #         t.append(array_datapoints[i + j].data_medianed)
        #     array_datapoints[i].data_3hr_avg = mean(t)

        # Calculate the tail end of the running average outside the window
        # using a simple linear approximation
        start = len(array_datapoints) - halfwindow_average -1
        finish = len(array_datapoints)

        t = []
        initial_value = array_datapoints[start].data_3hr_avg
        t.append(initial_value)
        for i in range(start, finish):
            if array_datapoints[i].data_medianed != 0:
                t.append(array_datapoints[i].data_medianed)
        increment = (t[len(t) - 1] - t[0]) / len(t)
        for i in range(start, finish):
            if array_datapoints[i].data_medianed != 0:
                array_datapoints[i].data_3hr_avg = initial_value
                initial_value = initial_value + increment

        # Calculate the residuals
        for dp in array_datapoints:
            if dp.data_3hr_avg != 0:
                if dp.data_medianed !=0:
                    dp.residual = dp.data_medianed - dp.data_3hr_avg

        # Create files for plotting
        d_time = []
        d_dtrend = []
        d_median = []
        d_average = []

        for d in array_datapoints:
            tt = standard_stuff.posix2utc(d.posixtime, '%Y-%m-%d %H:%M:%S')
            d_time.append(tt)
            d_dtrend.append(d.residual)
            d_median.append(d.data_medianed)
            d_average.append(d.data_3hr_avg)

        # For plotting we should remove the default zero value and use a null
        d_dtrend = remove_zeros(d_dtrend)
        d_median = remove_zeros(d_median)
        d_average = remove_zeros(d_average)

        savefile = publishdirectory + os.sep + "plot_detrend.jpg"
        title = "Geomagnetic Field: Detrended Horizontal Component. "
        plot(d_time, d_dtrend, None, title, savefile)

        savefile = publishdirectory + os.sep + "plot_dt_med.jpg"
        title = "Geomagnetic Field: Horizontal Component and 3hr Average. "
        plot(d_time, d_median, d_average, title, savefile)
