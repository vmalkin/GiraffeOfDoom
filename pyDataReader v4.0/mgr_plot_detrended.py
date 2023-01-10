import os
from time import time
from statistics import mean
import standard_stuff
import sqlite3
from plotly import graph_objects as go

class DataPoint:
    def __init__(self):
        pass

def plot(dt_dates, dt_detrend, average, savefile_name):
    width = 1500
    height = 500
    backgroundcolour = "#ffffff"
    pencolour = "#600000"
    gridcolour = "#909090"

    plotdata = go.Scatter(x=dt_dates, y=dt_detrend, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title="H-Component - Detrended",
                      xaxis_title="Date/time UTC<br><sub>http://RuruObservatory.org.nz</sub>",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")

    if average is not None:
        fig.add_scatter(x=dt_dates, y=average, mode="lines", connectgaps=True,
                        line=dict(color="#007090", width=3))

    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)

    fig.write_image(savefile_name)


def getposixtime():
    timevalue = int(time())
    return timevalue


def database_get_data(dba):
    tempdata = []
    # Grab a bit more than a day so we can do the running average with a bit of lead data
    starttime = getposixtime() - 91800
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

def wrapper(database, publishdirectory):
