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


def plot_chart(filename, dates, aggregatedata):
    fig = go.Figure()
    fig.update_yaxes(range=[5, 30])
    max = len(aggregatedata)
    for i in range(0, max):
        fig.add_scatter(x=dates, y=aggregatedata[i], mode="lines", connectgaps=True,
                        line=dict(color='rgba(0, 0, 0, 0.2)'))
        if i == max - 1:
            fig.add_scatter(x=dates, y=aggregatedata[i], mode="lines", connectgaps=True,
                            line=dict(color='rgba(255, 0, 0, 1)'))
    fig.update_layout(width=1400, height=600, title="GPS Noise",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="S4 Index",
                      plot_bgcolor="#e0e0e0")
    fig.write_image(file=filename, format='jpg')
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
        if item[index_alt] >= alt_min:
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
    print(len(aggregate_data[1]))


    # Generate list of hours/mins for plotter
    aggregate_dates = []
    # aggregate_data = []
    for i in range(0, 86400):
        aggregate_dates.append(posix2utc(i, "%H:%M"))
        # aggregate_dates.append(i)

    plot_chart("s4_aggregate.jpg", aggregate_dates, aggregate_data)

