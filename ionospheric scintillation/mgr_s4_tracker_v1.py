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
    print("Parsing database...")
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


def plot_chart(filename, dates, aggregatedata, avg_reading):
    fig = go.Figure()
    fig.update_yaxes(range=[5, 30])
    max = len(aggregatedata)
    for i in range(0, max):
        fig.add_scatter(x=dates, y=aggregatedata[i], opacity=0.6)
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
    index_s4 = 2
    index_alt = 1
    for item in queryresult:
        if item[index_alt] >= alt_min:
            if item[index_s4] >= s4_min:
                if item[index_s4] <= s4_max:
                    returnlist.append(item)
    return returnlist


# Create an overlapping plot of the past x days to show re-occuring daily features in S4 data
def wrapper(query_interval):
    querydata = database_parse(query_interval)
    print(querydata[2])
    # parse out readings < 40deg in alt and 0 < s4 < 100
    # parsed_query = query_parse(querydata)




    # plot_chart("s4_values.jpg", aggregate_dates, aggregate_data, 0)

