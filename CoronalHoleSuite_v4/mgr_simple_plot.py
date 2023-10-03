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


def plot(plotlist, trend):
    pass


def create_trend(plotlist):
    return []


def create_splitdata(plotlist, starttime, carrington_rotations):
    # data is at 1 min intervals
    tempdata = []

    # round the start to the nearest whole minute, if we are to match with timestamps in data
    # CREATE the empty array, 1 minute intervals, for the carrington rotation period, to store solar wind data
    #  for plotting
    starttime = int(starttime / 60) * 60
    for i in range(int(starttime), int(starttime + carrington_rotations), 60):
        dp = [i, None]
        tempdata.append(dp)

    # implement hash function to drop data into the correct slot based on posix time
    for item in plotlist:
        index = int((item[0] - starttime) / 60)
        # j = item.split(",")
        tempdata[index][1] = item[1]

    # We now have an array with the correct number of slots for the time, and data dropped into the correct slots
    # and some slots will have null values if there is no data for that particular time.
    # Divide that data into segments one carrington rotation long. This will create an array of arrays that
    # will get returned to be passed into the plotter, and used to calculate the simple prediction for the next
    # carrington rotation.

    step = k.carrington_rotation * 1440
    lower = starttime
    upper = lower + step
    returnlist = []
    tmp = []

    for i in range(0, len(tempdata)):
        if i >= lower:
            if i < upper:
                # just the data value
                tmp.append(tempdata[i][1])

        if i >= upper:
            step_multiple = step_multiple + 1
            lower = upper
            upper = step_multiple * step
            returnlist.append(tmp)
            tmp = []
            # just the data value
            tmp.append(tempdata[i][1])

        if i == (len(tempdata) - 1):
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
    plotlist = []
    data = db_getdata(starttime, "dscovr")
    for item in data:
        if item[0] > starttime:
            dp = [item[0], item[2]]
            plotlist.append(dp)

    splitdata = create_splitdata(plotlist, starttime, cr)

    for item in splitdata:
        print(item)


    # trend = create_trend(plotlist)
    # plot(splitdata, trend)

wrapper()
