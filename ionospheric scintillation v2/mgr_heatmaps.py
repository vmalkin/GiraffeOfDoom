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


class Dday:
    def __init__(self, datestring):
        self.hours = []
        self.label = datestring
        for i in range(0, 24):
            h = Dhours(i)
            self.hours.append(h)

class Dhours:
    def __init__(self, label):
        self.label = label
        self.minutes = []
        for i in range(0, 60):
            m = Dmins(i)
            self.minutes.append(m)


class Dmins:
    def __init__(self, label):
        self.label = label
        self.datavalue = []

    def get_average(self):
        returnresult = nullvalue
        if len(self.datavalue) > 0:
            returnresult = mean(self.datavalue)
        return returnresult

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

    data = go.Scatter()
    fig = go.Figure(data)
    title = "Signal to Noise Ratio for " + comport
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="SNR - dB",
                      plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )

    for item in displaydata:
        fig.add_trace(go.Scatter(x=timestamps, y=item))
    fig.write_image("stackplot.jpg")


def heatmap(displaydata, timestamps, label_day, comport):
    papercolour = "#000000"
    gridcolour = "#303030"
    width = 1500

    data = go.Heatmap(x=timestamps, y=label_day, colorscale = 'electric')
    fig = go.Figure(data)

    title = "Heatmap, SNR for " + comport
    fig.update_layout(width=width, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="SNR - dB")

    # for item in displaydata:
    #     fig.add_trace(go.Scatter(x=timestamps, y=item))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )
    fig.update_layout(plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)

    for item in displaydata:
        print(item)
        fig.add_trace(go.Heatmap(x=timestamps, y=label_day, z=item, colorscale = 'electric'))

    fig.write_image("heatmap.jpg")


def wrapper(result, comport):
    # utctime = "2023-02-20 00:00"
    # starttime = utc2posix(utctime, '%Y-%m-%d %H:%M')
    # day = 60 * 60 * 24 * 14
    # actualstart = starttime - day
    #
    # alt = 40
    # # The result of the query gets passed into all plotting functions
    # result = mgr_database.qry_get_last_24hrs(actualstart, alt)
    # result = np.array(result)

    start = int(result[0][1])
    end = int(result[len(result) - 1][1])
    day = 60 * 60 * 24
    # duration = (end - start) / day
    # duration = math.ceil(duration)

    days = []
    for i in range(start, end, day):
        dd = Dday(i)
        days.append(dd)

    # Populate the day objects with data
    for row in result:
        psx = int(row[1])
        data = float(row[5])
        hr = int(posix2utc(psx, '%H'))
        mn = int(posix2utc(psx, '%M'))
        idx = int(math.floor((psx - start) / day))
        days[idx].hours[hr].minutes[mn].datavalue.append(data)
        # print(days[idx].hours[hr].minutes[mn].get_average())

    displaydata = []
    timestamps = []
    for i in range(0, 24):
        for j in range(0, 60):
            k = j
            if k < 10:
                k = '0' + str(k)
            else:
                k = str(k)

            timestring = str(i) + ":" + str(k)
            timestamps.append(timestring)

    # Create the day lables. the y axis of the heatmap
    daylabels = []
    for dd in days:
        daylabels.append(posix2utc(dd.label, "%Y-%m-%d"))

    # Create the arrays of each days minute data
    for dd in days:
        temparray = []
        for i in range(0, 1440):
            temparray.append(None)

        for hour in dd.hours:
            for minute in hour.minutes:
                idx = int(hour.label) * int(minute.label)
                data = minute.get_average()
                temparray[idx] = data
                ts = str(hour.label) + ":" + str(minute.label)
                timestamps.append(ts)
        displaydata.append(temparray)

    stackplot(displaydata, timestamps, daylabels, comport)
    # heatmap(displaydata, timestamps, daylabels, comport)

# mgr_plot.wrapper(result, k.comport)