import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import time
import emd
import numpy as np
import os
import sqlite3
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def getposixtime():
    timevalue = int(time.time())
    return timevalue


def database_get_data(dba, starttime):
    tempdata = []
    # Grab a bit more than a day so we can do the running average with a bit of lead data
    # starttime = getposixtime() - 86400
    db = sqlite3.connect(dba)
    try:
        cursor = db.cursor()
        result = cursor.execute("select * from data where data.posixtime > ? order by data.posixtime asc", [starttime])
        for line in result:
            dt = line[0]
            da = line[1]
            d = [dt, da]
            tempdata.append(d)

    except sqlite3.OperationalError:
        print("Database is locked, try again!")
    db.close()
    return tempdata

def plot_data(imf, dates, filename):
    backgroundcolour = "#ffffff"
    pencolour = "#600000"
    gridcolour = "#909090"

    rownum = imf.shape[1]
    plot_height = rownum * 300
    fig = make_subplots(rows=rownum, cols=1)
    title = "Empirical Mode Decomposion: H Component data. "
    title = title + "<i>Updated " + posix2utc(time.time(), '%Y-%m-%d %H:%M') + "</i>"

    iters = len(imf[0])
    for i in range(0, iters):
        fig.add_trace(go.Scatter(x=dates, y=imf[:, i], mode="lines", line=dict(color=pencolour, width=2)),
                      row=i+1, col=1)
        # fig.add_trace(go.Scatter(x=dates, y=imf[:, i], mode="lines", line=dict(color=pencolour, width=2)),
        #               row=i+1, col=1)


    fig.update_layout(height=plot_height, width=1500, title_text=title)
    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_layout(showlegend=False,
                      font_family="Courier New")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                     zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
    fig.write_image(filename)
    fig.write_html("publish/plot_emd.html")

def wrapper(data, publishdirectory):
    readings = data

    dt_dates = []
    dt_readings = []
    for item in readings:
        date = posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
        dt_dates.append(date)
        reading = item[1]
        dt_readings.append(reading)

    print(len(dt_dates), len(dt_readings))
    nn = np.array(dt_readings, dtype='float')

    # imf = emd.sift.iterated_mask_sift(n)
    # imf = emd.sift.complete_ensemble_sift(nn)
    imf = emd.sift.sift(nn)

    savefile = publishdirectory + os.sep + "plot_emd.jpg"
    plot_data(imf, dt_dates, savefile)



