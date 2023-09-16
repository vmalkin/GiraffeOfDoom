# THis will generate a simple line plot of solar wind speed for the last 3 carrington rotations
# and highlight repeating events.

import common_data as k
import sqlite3
import time
import datetime
from plotly import graph_objects as go

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


def create_splitdata(plotlist):
    pass


def wrapper():
    # start date is three Carington Rotati0ns ago.
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

    trend = create_trend(plotlist)
    splitdata = create_splitdata(plotlist)
    plot(splitdata, trend)



