import constants as k
import datetime
import time
import plotly.graph_objects as go
from statistics import mean, stdev, median
import json

sat_database = "gps_satellites.db"
nullvalue = "none"


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def indexposition(posixtime, starttime):
    interval = posixtime - starttime
    interval = int(interval / 60)
    return interval


def plot_chart(filename, dates, aggregatedata, avg_reading):
    fig = go.Figure()
    fig.update_yaxes(range=[5, 30])
    max = len(aggregatedata)
    for i in range(0, max):
        fig.add_scatter(x=dates, y=aggregatedata[i], opacity=0.3)
        if i == max - 1:
            fig.add_scatter(x=dates, y=aggregatedata[i], line=dict(color='rgba(0, 0, 0, 1)'))
    # fig = go.Figure(go.Scatter(x=dates, y=data, mode="markers", trendline="rolling", trendline_options=dict(window=20)))
    # fig.write_image(file=savefile, format='jpg')
    fig.show()


def query_parse(queryresult):
    """
    Filter the raw query result
    """
    s4_min = 0
    s4_max = 200
    alt_min = 40
    returnlist = []
    index_s4 = 4
    index_alt = 2
    for item in queryresult:
        if item[index_alt] >= alt_min:
            if item[index_s4] >= s4_min:
                if item[index_s4] <= s4_max:
                    returnlist.append(item)
    return returnlist


# Create an overlapping plot of the past x days to show re-occuring daily features in S4 data
def wrapper(querydata):
    # parse out readings < 40deg in alt and 0 < s4 < 100
    parsed_query = query_parse(querydata)
    half_window = 10
    old_x_data = []
    old_y_data = []
    tmp = [0]

    # Create first pass thru data - average value for each minute
    for i in range(0, len(parsed_query) - 1):
        dt = parsed_query[i][1]
        dv = parsed_query[i][4]
        tmp.append(dv)

        t1 = posix2utc(parsed_query[i][1], '%Y-%m-%d %H:%M')
        t2 = posix2utc(parsed_query[i + 1][1], '%Y-%m-%d %H:%M')

        if t1 != t2:
            old_x_data.append(parsed_query[i][1])
            old_y_data.append(mean(tmp))
            tmp = []

    # Smooth the data
    x_data = []
    y_data = []
    t = []
    for i in range(0, len(old_y_data)):
        t.append(old_y_data[i])
        if len(t) > half_window * 2:
            t.pop(0)
            d = mean(t)
            y_data.append(d)
            x_data.append(old_x_data[i - half_window])

    print("Length of First pass dates: ", len(x_data))
    print("Length of First pass data: ", len(y_data))

    # rearrange the data to create a stacked trace.
    aggregate_data = []
    aggregate_dates = []
    tmp = []
    for i in range(0, len(x_data) - 1):
        tmp.append(y_data[i])
        t1 = posix2utc(x_data[i], "%Y-%m-%d")
        t2 = posix2utc(x_data[i + 1], "%Y-%m-%d")
        if t1 != t2:
            aggregate_data.append(tmp)
            tmp = []

    for i in range(0, 1440):
        d = posix2utc(x_data[i], "%H:%M")
        aggregate_dates.append(d)

    print(len(aggregate_dates))
    print(len(aggregate_data[1]))

    plot_chart("s4_values.jpg", aggregate_dates, aggregate_data, 0)

