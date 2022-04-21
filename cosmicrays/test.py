import mgr_plot_simple_avg
import mgr_plot_avg_hits
import sqlite3
import time
import datetime
import mgr_emd

database = "events.db"

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(value):
    # dateformat = "%Y-%m-%d %H:%M:%S.%f"
    dateformat = "%Y-%m-%d %H:%M:%S"
    newdatetime = datetime.datetime.strptime(value, dateformat)
    newdatetime = time.mktime(newdatetime.timetuple())
    newdatetime = int(newdatetime)
    return newdatetime


def database_get_data(hours_duration):
    duration = hours_duration * 3600
    tempdata = []
    starttime = int(time.time()) - duration
    db = sqlite3.connect(database)
    cursor = db.cursor()
    result = cursor.execute("select posixtime from data where posixtime > ? order by posixtime asc", [starttime])
    for line in result:
        d = line[0]
        tempdata.append(d)
    db.close()
    return tempdata

# data = []
# file = "dr01_24hr.csv"
# with open(file, "r") as f:
#     for line in f:
#         line = line.rstrip("\n")
#         l = line.split(",")
#         dt = utc2posix(l[0])
#         da = l[1]
#         dp = str(dt) + "," + str(da)
#         data.append(dp)

data = database_get_data(24*30)

with open("analysis.csv", "w") as a:
    for item in data:
        tp = item
        tt = posix2utc(tp, "%Y-%m-%d %H:%M:%S")
        dp = tt + "," + str(tp)
        a.write(dp + "\n")
a.close()
