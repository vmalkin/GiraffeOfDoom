# THis will generate a simple line plot of solar wind speed for the last 3 carrington rotations
# and highlight repeating events.

import common_data as k
import sqlite3
import time
import datetime
from plotly import graph_objects as go
import numpy as np

def db_getdata(starttime, satellite_name):
    returnvalues = []
    item = [starttime, satellite_name]
    db = sqlite3.connect(k.database)
    cursor = db.cursor()
    cursor.execute("select * from sw_data where sw_data.sw_time > ? and sw_data.sat_id = ?", item)
    for item in cursor.fetchall():
        returnvalues.append(item)
    return returnvalues


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def plot(splitlist):
    plotdata = go.Scatter(mode="lines")
    fig = go.Figure(plotdata)

    for item in splitlist:
        tmp = []
        for d in item:
            data = d[1]
            tmp.append(data)
        fig.add_trace(go.Scatter(y=tmp, mode="lines"))
    fig.show()


def create_trend(plotlist):
    return []

def posixdate_roundto_minute(value):
    # Round a posix date down to the nearest minute
    i = int(value / 60) * 60
    return i


def split_plotarray(plotarray, starttime, endtime):
    step = (86400 * k.carrington_rotation)
    step = posixdate_roundto_minute(step)
    lower = starttime
    upper = lower + step

    returnlist = []
    tmp = []

    for i in range(0, len(plotarray)):
        plotdate = plotarray[i][0]
        if plotdate >= lower:
            if plotdate < upper:
                tmp.append(plotarray[i])

        if plotdate >= upper:
            # step_multiple = step_multiple + 1
            lower = upper
            upper = upper + step
            returnlist.append(tmp)
            tmp = []
            tmp.append(plotarray[i])

        if plotdate == (endtime - 1):
            returnlist.append(tmp)
    return returnlist

def wrapper():
    # start date is three Carington Rotations ago.
    # A day is 86400 seconds long
    day = 86400
    cr = 3 * k.carrington_rotation * day

    # data format:
    # [1693631580, None, 547.1, 0.18, sat_id]
    starttime = time.time() - cr
    starttime = posixdate_roundto_minute(starttime)

    endtime = starttime + cr
    endtime = posixdate_roundto_minute(endtime)

    prunedlist = []
    data = db_getdata(starttime, "dscovr")

    # Prune data to only have posixtime and solar wind speed
    for item in data:
        if item[0] > starttime:
            dp = [item[0], item[2]]
            prunedlist.append(dp)

    # Create a Dictionary of the last three Carrington rotations. This will have the dates, but be empty
    plotarray = {}
    for i in range(starttime, endtime, 60):
        plotarray[i] = None

    # Populate the array of Carrington rotations with data from the database.
    for item in prunedlist:
        date = item[0]
        data = item[1]
        plotarray[date] = data

    # Split the array from [all data], to [[rotation 1], [rotation 2], [rotation 3]] based on the dates.
    splitdata = split_plotarray(plotarray, starttime, endtime)

    # trend = create_trend(plotlist)
    plot(splitdata)

wrapper()
