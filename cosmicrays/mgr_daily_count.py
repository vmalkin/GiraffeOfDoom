from statistics import mean, stdev
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


def running_avg(series):
    returnarray = []
    returnarray.append(None)
    for i in range(1, len(series) - 1):
        t = []
        for j in range(-1, 2):
            t.append(series[i + j])
        tt = round(mean(t), 4)
        returnarray.append(tt)
    returnarray.append(None)
    return returnarray


def plot(dates, data):
    avg_data = running_avg(data)
    mn = mean(data)
    sig_1 = mn - stdev(data) * 2
    sig_4 = mn + stdev(data) * 2
    sig_2 = mn - stdev(data) * 1
    sig_3 = mn + stdev(data) * 1

    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker=dict(color='#89BFD6', opacity=0.8,
                                       line=dict(width=1, color="blue")),
                           name="Count"))

    fig.add_hline(y=mn, line=dict(width=6, color='green'), layer="below", annotation_text="Average")
    fig.add_hrect(y0=sig_2, y1=sig_3, line_width=0, fillcolor="green", opacity=0.3, layer="below",
                  annotation_text="± 1 StdDev")
    fig.add_hrect(y0=sig_1, y1=sig_4, line_width=0, fillcolor="green", opacity=0.3, layer="below",
                  annotation_text="± 2 StdDev")

    fig.add_trace(go.Scatter(x = dates, y = avg_data,
                             line=dict(color='black', width=4),
                             name="3 Day Avg"))

    fig.update_xaxes(ticks='outside', tickangle=45)
    # fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(legend=dict(yanchor="top", y=1.2,
                                  xanchor="left", x=0.85,
                                  orientation="h"))
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#c0c0c0", paper_bgcolor="#c0c0c0")
    fig.update_layout(width=1400, height=600,
                      title="Muons - Daily count",
                      yaxis_title="Daily Count",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    # title = "muons_avg_" + str(hrs) + "_hr.jpg"
    fig.write_image("muon_daily.jpg")


def wrapper():
    data = database_get_data(24*60)
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
