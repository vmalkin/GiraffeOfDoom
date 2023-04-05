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
        self.mins = []
        self.label = datestring
        for i in range(0, 1440):
            self.mins.append([])




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
        fig.add_trace(go.Scatter(x=timestamps, y=item, mode='lines'))

    fig.write_image("stackplot.jpg")


def heatmap(displaydata, timestamps, label_day, comport):
    papercolour = "#000000"
    gridcolour = "#303030"
    width = 1500

    # # CReate individual heatmap traces
    # data = []
    # for item in displaydata:
    #     trace = go.Heatmap(x=timestamps, y=label_day, z=item)
    #     data.append(trace)

    data = go.Heatmap(x=timestamps, y=label_day, z=displaydata, colorscale="electric")
    fig = go.Figure(data=data)

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

    fig.show()

    # fig.write_image("heatmap.jpg")


def wrapper(result, comport):
    start = int(result[0][1])
    end = int(result[len(result) - 1][1])
    day = 60 * 60 * 24
    # duration = (end - start) / day
    # duration = math.ceil(duration)



    stackplot(displaydata, timestamps, daylabels, comport)
    heatmap(displaydata, timestamps, daylabels, comport)

    with open("data.csv", "w") as d:
        for item in result:
            dd = posix2utc(item[1], "%Y-%m-%d %H:%M:%S")
            da = item[5]
            dp = dd + "," + da + "\n"
            d.write(dp)
    d.close()

# mgr_plot.wrapper(result, k.comport)