from statistics import mean, stdev
import sqlite3
import time
import datetime
from plotly import graph_objects as go

database = "events.db"


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
    mn = mean(data)
    sig_1 = mn - stdev(data) * 2
    sig_2 = mn - stdev(data) * 1
    sig_3 = mn + stdev(data) * 1
    sig_4 = mn + stdev(data) * 2


    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker=dict(color='#340059', line=dict(width=0.5, color='#340059'))))
    fig.add_hline(y=sig_1)
    fig.add_hline(y=sig_2)
    fig.add_hline(y=mn)
    fig.add_hline(y=sig_3)
    fig.add_hline(y=sig_4)

    fig.update_xaxes(ticks='outside', tickangle=45)
    # fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=600,
                      title="Muons - Daily count",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    # title = "muons_avg_" + str(hrs) + "_hr.jpg"
    fig.write_image("t_muon_daily.jpg")

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


data = database_get_data(24 * 60)
# data = [10,20,30,40]
data_counts = []
data_times = []
tmp = []
for i in range(0, len(data) - 1):
    if posix2utc(data[i + 1], "%d") == posix2utc(data[i], "%d"):
        # print("Match", i, len(data))
        tmp.append(1)

    if posix2utc(data[i + 1], "%d") != posix2utc(data[i], "%d"):
        # print("Not Match", i, len(data))
        tmp.append(1)
        tt = posix2utc(data[i], "%Y-%m-%d")
        dd = sum(tmp)
        data_counts.append(dd)
        data_times.append(tt)
        tmp = []

    if i == len(data) - 2:
        # print("End", i, len(data))
        tmp.append(1)
        tt = posix2utc(data[i], "%Y-%m-%d")
        dd = sum(tmp)
        data_counts.append(dd)
        data_times.append(tt)

plot(data_times, data_counts)

