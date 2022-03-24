import constants as k
import datetime
import time
import plotly.graph_objects as go
from statistics import mean, stdev, median
import sqlite3
import json

sat_database = "gps_satellites.db"
nullvalue = "none"
optimum_altitude = 25


def database_parse(hourduration):
    starttime = int(time.time()) - (60 * 60 * hourduration)
    print("Querying database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select posixtime, alt, avg(s4) from satdata where posixtime > ? and alt > ? group by posixtime order by posixtime asc', [starttime, optimum_altitude])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def indexposition(posixtime, starttime):
    interval = posixtime - starttime
    interval = int(interval / 60)
    return interval


def plot_chart(filename, dates, aggregatedata, seriesnames):
    # Colours set up for a max of ten days of data!

    filename = k.dir_images + "/" + filename
    bkcolour = "#e0e0e0"
    gridcolour = "#d0d0d0"
    colourdict = [
        "rgba(79,208,168,0.6)",
        "rgba(193,166,67,0.6)",
        "rgba(123,177,91,0.6)",
        "rgba(192,105,186,0.6)",
        "rgba(108,123,213,0.6)",
        "rgba(184,85,60,0.6)",
        "rgba(185,74,115,0.6)",
        "rgba(81,44,123,0.6)"
    ]
    sundict = [
        [291, 1231],
        [331, 1211],
        [373, 1227],
        [415, 1168],
        [454, 1056],
        [483, 1022],
        [500, 1023],
        [477, 1051],
        [427, 1088],
        [370, 1125],
        [315, 1168],
        [283, 1209]
    ]
    month_number = int(posix2utc(time.time(), "%m"))
    fig = go.Figure()
    fig.update_yaxes(range=[8, 26], gridcolor=gridcolour)
    fig.update_xaxes(nticks=48, tickangle=45, gridcolor=gridcolour)

    fig.add_vline(x=sundict[month_number][0], annotation_text=" &#9790; ", annotation_position="top right",
                  line_width=2, line_color="blue", annotation_font=dict(size=50, color="blue"))
    fig.add_vline(x=sundict[month_number][1], annotation_text=" &#9788; ", annotation_position="top left",
                  line_width=2, line_color="orangered", annotation_font=dict(size=50, color="orangered"))

    max = len(aggregatedata)
    for i in range(0, max):
        # all previous readings
        if i < max - 3:
            fig.add_scatter(x=dates, y=aggregatedata[i], mode="lines", connectgaps=True,
                            name=seriesnames[i], line=dict(color=colourdict[i], width=2))
        # Yesterday's reading
        if i == max - 2:
            fig.add_scatter(x=dates, y=aggregatedata[i], mode="lines", connectgaps=True,
                            name=seriesnames[i], line=dict(color='rgba(255, 0, 0, 1)', width=4))
        # Today's reading
        if i == max - 1:
            fig.add_scatter(x=dates, y=aggregatedata[i], mode="lines", connectgaps=True,
                            name=seriesnames[i], line=dict(color='rgba(0, 0, 0, 1)', width=4))

    fig.update_layout(width=1500, height=600, title="S4 index (GPS Noise). http://DunedinAurora.NZ",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="S4 Index",
                      plot_bgcolor="#e0e0e0")
    fig.update_layout(plot_bgcolor=bkcolour, paper_bgcolor=bkcolour)
    fig.write_image(file=filename, format='svg')
    # fig.show()


def query_parse(queryresult):
    """
    Filter the raw query result
    """
    # s4_min = 0
    # s4_max = 200
    alt_min = 30
    returnlist = []
    index_s4 = 2
    index_alt = 1
    for item in queryresult:
        # if item[index_alt] >= alt_min:
            # if item[index_s4] >= s4_min:
            #     if item[index_s4] <= s4_max:
        dt = item[0]
        dd = item[2]
        d = [dt, dd]
        returnlist.append(d)
    return returnlist


def medianfilter(parsed_query):
    # (1647323803, 20.124772)
    returnlist = []
    for i in range(1, len(parsed_query) - 1):
        dt = parsed_query[i][0]
        t = []
        t.append(parsed_query[i - 1][1])
        t.append(parsed_query[i][1])
        t.append(parsed_query[i + 1][1])
        dv = median(t)
        d = [dt, dv]
        returnlist.append(d)
    return returnlist


def runningavg(parsed_query):
    # [1647325304, 14.299302]
    halfwindow = 10
    returnlist = []
    temp = []
    for i in range(0, len(parsed_query)):
        data = parsed_query[i][1]
        temp.append(data)
        if len(temp) > halfwindow * 2:
            temp.pop(0)
            dd = mean(temp)
            dt = parsed_query[i - halfwindow][0]
            d = [dt, dd]
            returnlist.append(d)
    return returnlist


# Create an overlapping plot of the past x days to show re-occuring daily features in S4 data
def wrapper(query_interval):
    querydata = database_parse(query_interval)
    # parse out readings < 40deg in alt and 0 < s4 < 100
    parsed_query = query_parse(querydata)

    # Remove spikes with Median Filter
    parsed_query = medianfilter(parsed_query)

    # SMooth data with a running avg
    parsed_query = runningavg(parsed_query)

    # Slice data by UTC days and created stacked lists for plotting
    null = None
    aggregate_data = []
    tmp = []

    for j in range(0, 86400):
        tmp.append(null)

    for i in range(0, len(parsed_query) - 1):
        t1 = parsed_query[i][0] % 86400
        t2 = parsed_query[i + 1][0] % 86400
        tmp[t1] = parsed_query[i][1]
        if t1 - t2 > 70000:
            aggregate_data.append(tmp)
            tmp = []
            for j in range(0, 86400):
                tmp.append(null)
    aggregate_data.append(tmp)

    # Generate list of hours/mins for plotter
    aggregate_dates = []
    for i in range(0, 86400):
        aggregate_dates.append(posix2utc(i, "%H:%M"))

    # generate a list of dates for the legend
    datelist = []
    d0 = posix2utc(parsed_query[0][0], "%b-%d")
    datelist.append(d0)
    for item in parsed_query:
        d1 = posix2utc(item[0], "%b-%d")
        if d0 != d1:
            datelist.append(d1)
            d0 = d1

    plot_chart("s4_aggregate.svg", aggregate_dates, aggregate_data, datelist)

