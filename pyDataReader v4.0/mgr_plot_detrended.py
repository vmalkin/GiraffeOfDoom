import os
from time import time
from statistics import mean, median
import standard_stuff
import sqlite3
from plotly import graph_objects as go

null_value = f'null'
halfwindow_median = 8
halfwindow_average = int(30 * 60 * 1.5)

class DataPoint:
    def __init__(self):
        self.posixtime = 0
        self.data_raw = 0
        self.data_medianed = 0
        self.data_avg = 0
        self.residual = 0

def plot(dates, data1, data2, title, savefile_name):
    width = 1500
    height = 500
    backgroundcolour = "#ffffff"
    pencolour = "#600000"
    gridcolour = "#909090"

    plotdata = go.Scatter(x=dates, y=data1, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br>http://RuruObservatory.org.nz",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")

    if data2 is not None:
        fig.add_scatter(x=dates, y=data2, mode="lines", connectgaps=False,
                        line=dict(color="#0080f0", width=3))

    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                     zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
    fig.update_xaxes(nticks=24, ticks='outside',
                     tickangle=45, tickformat="%b %d, %H:%M")
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

    if len(readings) > halfwindow_average * 2:
        # Create datapont array
        array_datapoints = []
        for item in readings:
            d = DataPoint()
            d.posixtime = item[0]
            d.data_raw = item[1]
            array_datapoints.append(d)

        # find median value for each datapoint

        for i in range(halfwindow_median, len(array_datapoints) - halfwindow_median):
            t = []
            for j in range(-halfwindow_median, halfwindow_median):
                t.append(array_datapoints[i + j].data_raw)
            x = median(t)
            array_datapoints[i].data_medianed = x

        # Calculate the running average using a 3 hour window

        t = []
        for i in range(0, len(array_datapoints)):
            t.append(array_datapoints[i].data_medianed)
            if len(t) >= 2 * halfwindow_average:
                array_datapoints[i - halfwindow_average].data_avg = mean(t)
                t.pop(0)
        # Calculate the tail end of the running average outside the window
        # using a simple linear approximation
        start = len(array_datapoints) - halfwindow_average - 1
        finish = len(array_datapoints)
        t = []
        initial_value = array_datapoints[start].data_avg
        t.append(initial_value)
        for i in range(start, finish):
            if array_datapoints[i].data_medianed != 0:
                t.append(array_datapoints[i].data_medianed)
        increment = (t[len(t) - 1] - t[0]) / len(t)
        for i in range(start, finish):
            if array_datapoints[i].data_medianed != 0:
                array_datapoints[i].data_avg = initial_value
                initial_value = initial_value + increment

        # Calculate the residuals
        for dp in array_datapoints:
            if dp.data_avg != 0:
                if dp.data_medianed !=0:
                    dp.residual = dp.data_medianed - dp.data_avg

        # Create files for plotting
        d_time = []
        d_dtrend = []
        d_median = []
        d_average = []

        for d in array_datapoints:
            tt = standard_stuff.posix2utc(d.posixtime, '%Y-%m-%d %H:%M:%S')
            d_time.append(tt)

            if d.residual == 0:
                d_dtrend.append(null_value)
            else:
                d_dtrend.append(d.residual)

            if d.data_medianed == 0:
                d_median.append(null_value)
            else:
                d_median.append(d.data_medianed)

            if d.data_avg == 0:
                d_average.append(null_value)
            else:
                d_average.append(d.data_avg)

        savefile = publishdirectory + os.sep + "plot_detrend.jpg"
        title = "Geomagnetic Field: Detrended Horizontal Component"
        plot(d_time, d_dtrend, None, title, savefile)

        savefile = publishdirectory + os.sep + "plot_dt_med.jpg"
        title = "Geomagnetic Field: Horizontal Component and 3hr Average"
        plot(d_time, d_median, d_average, title, savefile)

        print("*** Detrended: FINISHED")