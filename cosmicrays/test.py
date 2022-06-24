from statistics import mean, stdev
import sqlite3
import time
import datetime
from plotly import graph_objects as go
import mgr_emd
#
# database = "events.db"
#
#
# def database_get_data(hours_duration):
#     duration = hours_duration * 3600
#     tempdata = []
#     starttime = int(time.time()) - duration
#     db = sqlite3.connect(database)
#     cursor = db.cursor()
#     result = cursor.execute("select posixtime from data where posixtime > ? order by posixtime asc", [starttime])
#     for line in result:
#         d = line[0]
#         tempdata.append(d)
#     db.close()
#     return tempdata
#
#
# def plot(dates, data):
#     avg_data = running_avg(data)
#     mn = mean(data)
#     sig_1 = mn - stdev(data) * 2
#     sig_2 = mn - stdev(data) * 1
#     sig_3 = mn + stdev(data) * 1
#     sig_4 = mn + stdev(data) * 2
#
#
#     fig = go.Figure(go.Bar(x=dates, y=data,
#                            marker=dict(color='#505050', line=dict(width=0.5, color='#505050')), name="hits per 24 hr"))
#     fig.add_trace(go.Scatter(x = dates, y = avg_data, name="3 Day Avg"))
#
#     fig.add_hline(y=sig_1, line=dict(width=2, color='orange'))
#     fig.add_hline(y=sig_2, line=dict(width=2, color='yellow'))
#     fig.add_hline(y=mn, line=dict(width=2, color='green'))
#     fig.add_hline(y=sig_3, line=dict(width=2, color='yellow'))
#     fig.add_hline(y=sig_4, line=dict(width=2, color='orange'))
#
#     fig.update_xaxes(ticks='outside', tickangle=45)
#     # fig.update_yaxes(range=[0, 1],  nticks=2)
#     fig.update_layout(font=dict(size=14), title_font_size=21)
#     fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
#     fig.update_layout(width=1400, height=600,
#                       title="Muons - Daily count",
#                       xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
#     # title = "muons_avg_" + str(hrs) + "_hr.jpg"
#     fig.write_image("t_muon_daily.jpg")
#
# def posix2utc(posixtime, timeformat):
#     # '%Y-%m-%d %H:%M'
#     utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
#     return utctime
#
# def running_avg(series):
#     returnarray = []
#     returnarray.append(None)
#     for i in range(1, len(series) - 1):
#         t = []
#         for j in range(-1, 2):
#             t.append(series[i + j])
#         tt = round(mean(t), 4)
#         returnarray.append(tt)
#     returnarray.append(None)
#     return returnarray
#
# data = database_get_data(24 * 365)
# # data = [10,20,30,40]
# data_counts = []
# data_times = []
# tmp = []
# for i in range(0, len(data) - 1):
#     if posix2utc(data[i + 1], "%d") == posix2utc(data[i], "%d"):
#         # print("Match", i, len(data))
#         tmp.append(1)
#
#     if posix2utc(data[i + 1], "%d") != posix2utc(data[i], "%d"):
#         # print("Not Match", i, len(data))
#         tmp.append(1)
#         tt = posix2utc(data[i], "%Y-%m-%d")
#         dd = sum(tmp)
#         data_counts.append(dd)
#         data_times.append(tt)
#         tmp = []
#
#     if i == len(data) - 2:
#         # print("End", i, len(data))
#         tmp.append(1)
#         tt = posix2utc(data[i], "%Y-%m-%d")
#         dd = sum(tmp)
#         data_counts.append(dd)
#         data_times.append(tt)
#
# mgr_emd.wrapper(data_counts, data_times, "test_emd.jpg")
# plot(data_times, data_counts)
#
database = "events.db"


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


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

def get_emd_data():
    data = database_get_data(24 * 365)
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

    returnvalue = []
    returnvalue.append(data_times)
    returnvalue.append(data_counts)
    return returnvalue


emd_data = get_emd_data()
datetimes = emd_data[0]
datavalues = emd_data[1]
mgr_emd.wrapper(datavalues, datetimes, "test_emd.jpg")