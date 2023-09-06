# THis will generate a simple line plot of solar wind speed for the last 3 carrington rotations
# and highlight repeating events.

import common_data as k
import sqlite3
import time
import datetime

def db_getdata(starttime):
    returnvalues = []
    item = [starttime]
    db = sqlite3.connect(k.database)
    cursor = db.cursor()
    cursor.execute("select * from sw_data where sw_data.sw_time > ?", item)
    for item in cursor.fetchall():
        returnvalues.append(item)
    return returnvalues


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def wrapper():
    # start date is three Carington Rotatins ago.
    day = 60 * 60 * 24
    cr = 3 * k.carrington_rotation * day
    # data format:
    # [1693631580, None, 547.1, 0.18]
    starttime = time.time() - cr
    plotlist = []
    data = db_getdata(starttime)
    for item in data:
        if item[0] > starttime:
            dp = [item[0], item[2]]
            plotlist.append(dp)



