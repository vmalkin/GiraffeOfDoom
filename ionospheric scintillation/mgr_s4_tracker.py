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


def plot_chart(filename, dates, data, avg_reading):
    fig = go.Figure(go.Scatter(x=dates, y=data, mode="lines"))
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
    print(parsed_query[0])

    x_data = []
    y_data = []
    tmp = [0]

    # Create first pass thru data - average value for each minute
    for i in range(0, len(parsed_query) - 1):
        dt = parsed_query[i][1]
        dv = parsed_query[i][4]
        dutc = posix2utc(dt, "%Y-%m-%d %H:%M")
        tmp.append(dv)

        if dt != parsed_query[i + 1][1]:
            x_data.append(dutc)
            y_data.append(mean(tmp))
            tmp = []
    print(len(x_data))

    plot_chart("s4_values.jpg", x_data, y_data, 0)
    # # create_json(report_data1440, ion_min, ion_max)
