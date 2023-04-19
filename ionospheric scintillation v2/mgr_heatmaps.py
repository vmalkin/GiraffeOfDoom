import time
import constants as k
import datetime
import math
import mgr_database
import mgr_plot
import numpy as np
from calendar import timegm
from statistics import mean, median
import plotly.graph_objects as go
nullvalue = None


class DayUTC:
    def __init__(self, utcdate, posixstart):
        self.utcdate = utcdate
        self.posixstart = posixstart

        self.data = []
        for i in range(0,1440):
            self.data.append([])

    def get_avg_array(self):
        returnarray = []
        for item in self.data:
            if len(item) == 0:
                returnarray.append(nullvalue)
            else:
                returnarray.append(mean(item))
        return returnarray

def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time

def stackplot(displaydata, timestamps, label_day, comport):
    width = 1500
    height = 600
    papercolour = "#000000"
    gridcolour = "#303030"
    dayssince = 7

    data = go.Scatter()
    fig = go.Figure(data)
    title = "Signal to Noise Ratio for " + comport + ". (dB). Last " + str(dayssince) + " days."
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="SNR - dB",
                      plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, showlegend=False)

    # ONLY show the last 7 days from the data

    for i in range(len(displaydata) - dayssince, len(displaydata) - 1):
        fig.add_trace(go.Scatter(x=timestamps, y=displaydata[i], mode='lines',
                                 line=dict(color="rgba(255,150,0,0.5)", width=2)
                                 ))
    lastindex = len(displaydata) - 1
    fig.add_trace(go.Scatter(x=timestamps, y=displaydata[lastindex], mode='lines',
                             line=dict(color="rgba(255,255,255,1)", width=2)
                             ))

    fig.write_image("stackplot.jpg")


def heatmap(displaydata, timestamps, label_day, comport):
    papercolour = "#000000"
    gridcolour = "#303030"
    width = 1500
    height = len(displaydata) * 25

    # # CReate individual heatmap traces
    # data = []
    # for item in displaydata:
    #     trace = go.Heatmap(x=timestamps, y=label_day, z=item)
    #     data.append(trace)

    data = go.Heatmap(x=timestamps, y=label_day, z=displaydata, colorscale="electric")
    fig = go.Figure(data=data)

    title = "Signal to Noise Ratio for " + comport + ". (dB)"
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")

    # for item in displaydata:
    #     fig.add_trace(go.Scatter(x=timestamps, y=item))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour, tickangle=50)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )
    fig.update_layout(plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    # fig.show()
    fig.write_image("heatmap.jpg")
    fig.write_html("heatmap.html")


def wrapper(result, comport):
    start = int(result[0][1])
    end = int(result[len(result) - 1][1])

    # CReate the array of UTC Day Objects to hold data
    array_days = []
    current_date = None
    for i in range(start, end):
        test_date = posix2utc(i, "%Y-%m-%d")
        if test_date == current_date:
            pass
        else:
            posixstart = i
            utcdate = test_date
            d = DayUTC(utcdate, posixstart)
            array_days.append(d)
        current_date = test_date

    # Start processing the results to place data in the correct day, and in the correct position in
    # the minutes of the day.
    for item in result:
        posixtime = item[1]
        data = item[5]

        # The day this data belongs in
        utcdate = posix2utc(posixtime, "%Y-%m-%d")
        posixday_start = utc2posix(utcdate, "%Y-%m-%d")

        # The index in the minute array of said day...
        minute_index = int((float(posixtime) - float(posixday_start)) / 60)

        # this is ugly, but append the data to the correct day and minute
        for item in array_days:
            if posixday_start == item.posixstart:
                item.data[minute_index].append(float(data))

    # Now iterate through our array of day objects, and populate the charting arrays, that are passed into
    # the charting functions.
    displaydata = []
    daylabels = []
    timestamps = []
    for item in array_days:
        daylabels.append(item.utcdate)
        displaydata.append(item.get_avg_array())

    daily_average_snr = []
    for item in displaydata:
        t = []
        for thing in item:
            if thing == None:
                pass
            else:
                t.append(thing)
        if len(t) > 0:
            avgitem = mean(t)
        else:
            avgitem = 0
        daily_average_snr.append(avgitem)


    # Create timestamps for horizontal axis
    for i in range(0, 1440):
        t = i / 60
        hr = int(t)
        mm = (t - hr) * 60
        mm = int(mm)
        hr = str(hr)
        mm = str(mm)
        if len(hr) == 1:
            hr = "0" + hr
        else:
            hr = hr

        if len(mm) == 1:
            mm = "0" + mm
        else:
            mm = mm
        timestamp = str(hr) + ":" + str(mm)
        timestamps.append(timestamp)

    stackplot(displaydata, timestamps, daylabels, comport)
    heatmap(displaydata, timestamps, daylabels, comport)
