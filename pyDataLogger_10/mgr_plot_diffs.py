from statistics import mean
import standard_stuff
import os
import sqlite3
from time import time
from plotly import graph_objects as go
import constants as k

# The number of readings that equates to one and a half hours of time.
half_window = 10


def plot(dt_dates, dt_detrend, savefile_name):
    width = k.plot_width
    height = k.plot_height
    backgroundcolour = k.plot_backgroundcolour
    pencolour = k.plot_pencolour
    gridcolour = k.plot_gridcolour

    title = "Geomagnetic Field: Smoothed dH/dt. "
    title = title +  "<i>Updated " + standard_stuff.posix2utc(time(), '%Y-%m-%d %H:%M') + "</i>"

    plotdata = go.Scatter(x=dt_dates, y=dt_detrend, mode="lines", line=dict(color=pencolour, width=2))
    fig = go.Figure(plotdata)
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br>http://RuruObservatory.org.nz",
                      yaxis_title="Magnetic Field Strength - Arbitrary Values")
    fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
    fig.update_layout(showlegend=False,
                      font_family="Courier New")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                     zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
    fig.update_xaxes(nticks=12, ticks='outside',
                     tickformat="%b %d<br>%H:%M")
    fig.write_image(savefile_name)



def getposixtime():
    timevalue = int(time())
    return timevalue


def database_get_data(dba, starttime):
    tempdata = []
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




def wrapper(data, publishdirectory):
    # THE DATALIST IS IN THE FORMAT "posixtime, data" We will need to split this into two lists
    # Dates and actual data.

    readings = data

    if len(readings) > half_window:
        savefile_name = publishdirectory + os.sep + "plot_dhdt.jpg"
        dt_dates = []
        dt_data = []
        # Calculate the rate of change.
        for i in range(1, len(readings) - 1):
            utcdate = standard_stuff.posix2utc(readings[i][0], '%Y-%m-%d %H:%M:%S')
            dt_dates.append(utcdate)
            d = float(readings[i][1]) - float(readings[i - 1][1])
            dt_data.append(float(d))

        # ########## Filtering and Adjustment before Plotting ##########
        # Smooth the data before plotting
        dt_data = standard_stuff.filter_median(dt_data, 3)
        dt_data = standard_stuff.filter_average(dt_data, 600)


        # the datetimes will be of a different length now because of the filtering of the data
        # Determin the difference and top and tail the datetimes array.
        # toptail = len(dt_dates) - len(dt_data)
        # dt_dates = dt_dates[toptail:-toptail]
        # ########## Filtering and Adjustment before Plotting ##########

        try:
            # print("*** dH/dt Magnetogram: Created")
            plot(dt_dates, dt_data, savefile_name)
        except:
            print("!!! Diurnal Magnetogram: FAILED to plot magnetogram")

