import sqlite3
import time
import datetime
from plotly import graph_objects as go

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

def plot(dates, data):
    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker=dict(color='#340059', line=dict(width=0.5, color='#340059'))))
    fig.update_xaxes(ticks='outside', tickangle=45)
    # fig.update_yaxes(range=[0, 1],  nticks=2)
    # fig.update_layout(font=dict(size=14), title_font_size=21)
    # fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    # fig.update_layout(width=1400, height=400,
    #                   title="Muons - Average Hits " + str(hrs) + " hour avg.",
    #                   xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    # title = "muons_avg_" + str(hrs) + "_hr.jpg"
    fig.show()


data = database_get_data(24*60)
data_counts = []
data_times = []
tmp = []
for i in range(0, len(data) - 1):
    if posix2utc(data[i + 1], "%d") == posix2utc(data[i], "%d"):
        tmp.append(1)

    if posix2utc(data[i + 1], "%d") != posix2utc(data[i], "%d"):
        tt = posix2utc(data[i], "%Y-%m-%d")
        dd = sum(tmp)
        data_counts.append(dd)
        data_times.append(tt)
        tmp = []

    if i == len(data) - 1:
        tt = posix2utc(data[i], "%Y-%m-%d")
        dd = sum(tmp)
        data_counts.append(dd)
        data_times.append(tt)

print(data_times, data_counts)
# plot(data_times, data_counts)
