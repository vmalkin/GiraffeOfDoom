import constants as k
import sqlite3
import datetime
import time
import plotly.graph_objects as go
from statistics import mean, stdev, median
import json

sat_database = "gps_satellites.db"
nullvalue = "none"

class Bin:
    def __init__(self, posixtime):
        self.time = posixtime

        # a count of s4 spikes
        self.data = [0]
    def median_data(self):
        if len(self.data) > 2:
            return median(self.data)
        else:
            return 0

    def average_data(self):
        return mean(self.data)

    def sumdata(self):
        return sum(self.data)

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def query_get_data(start):
    optimum_altitude = 40
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute(
        'select sat_id, posixtime, alt, az, s4, snr from satdata where posixtime > ? and alt > ? order by posixtime asc',
        [start, optimum_altitude])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4], item[5])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


def indexposition(posixtime, starttime):
    interval = posixtime - starttime
    interval = int(interval / 60)
    return interval


def plot_chart(filename, dates, data, avg_reading):
    black = "rgba(0,0,0,0.75)"
    savefile = k.dir_images + "//" + filename
    y_max = 20
    y_min = 5

    plotdata = go.Bar(x=dates, y=data, marker = dict(color=black, line=dict(width=1, color=black)))
    fig = go.Figure(plotdata)

    fig.add_trace(go.Scatter(x=dates, y=avg_reading, mode="lines", line=dict(width=6, color="#ffffff")))
    fig.add_trace(go.Scatter(x=dates, y=avg_reading, mode="lines", line=dict(width=3, color="#770000")))

    fig.update_xaxes(nticks=30, tickangle=45, gridcolor='#ffffff')
    fig.update_yaxes(range=[y_min ,y_max] )
    fig.update_layout(width=1400, height=600, title="S<sub>4</sub> Index - 1 minute bins & average trend",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="S<sub>4</sub> index, %",
                      plot_bgcolor="#e0e0e0")
    fig.update_layout(font=dict(size=18), title_font_size=22, showlegend=False)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    # fig.update_layout(width=1400, height=600)
    fig.write_image(file=savefile, format='jpg')
    # fig.show()


def query_parse(queryresult):
    """
    Filter the raw query result
    """
    s4_min = 0
    s4_max = 200
    alt_min = 40
    returnlist = []
    index_s4 = 4
    index_alt = 2
    for item in queryresult:
        if item[index_alt] >= alt_min:
            if item[index_s4] >= s4_min:
                if item[index_s4] <= s4_max:
                    returnlist.append(item)
    return returnlist


# def create_json(report_data, ion_min, ion_max):
#     result = "none"
#     dtm = int(time.time())
#
#     if len(report_data) > 60:
#         dtm = dtm
#         dta = report_data[-60:]
#         dta = mean(dta)
#
#         if dta < ion_min:
#             result = "none"
#
#         if dta > ion_min:
#             if dta <= ion_max:
#                 result = "low"
#
#         if dta > ion_max:
#             result = "high"
#
#     i = {"posixtime": dtm, "ionstate": result}
#     # print(dta, ion_min, ion_med, ion_max)
#     print(i)
#
#     filepath = "ion.json"
#     with open(filepath, "w") as j:
#         json.dump(i, j)


def calc_average(report_data):
    middle = []
    half_window = 10

    if len(report_data) > half_window * 2 + 1:
        for i in range(half_window, len(report_data) - half_window):
            temparray = []
            for j in range(0 - half_window, half_window):
                temparray.append(report_data[j + i])
            r = mean(temparray)
            middle.append(r)

    bookend = ["" for i in range(0, half_window)]

    returnarray = bookend + middle + bookend
    return returnarray



def wrapper():
    nowtime = int(time.time())
    posix_day = 60*60*24
    starttime = nowtime - (posix_day * 1)
    binlist = []

    # ion_max = 0
    # ion_min = 0
    # ion_average = 0

    # create the list of empty one minute bins
    bin_range = int((nowtime - starttime) / 60) + 1
    for i in range(0, bin_range):
        bintime = starttime + (i * 60)
        binlist.append(Bin(bintime))

    print("Length of binlist ", len(binlist))

    # get data for the required period (See value for variable starttime
    queryresult = query_get_data(starttime)

    # parse out readings below 40deg in alt and s4 over 100%
    parsed_query = query_parse(queryresult)

    # assign s4 readings to 1 minute bins in the correct range.
    for item in parsed_query:
        dt = item[1]
        i = indexposition(dt, starttime)
        if i >=0:
            if i <= bin_range - 1:
                binlist[i].data.append(item[4])  # add to the list

    # lists for plotting
    report_data = []
    report_datetime = []


    # Parse thru the list of bins, each entry in the report data represents a running cumulative total
    # of S4 spikes for the previous 24 hour period.
    for i in range(0, len(binlist)):
        x = binlist[i].average_data()
        dt = posix2utc(binlist[i].time, '%Y-%m-%d %H:%M')
        report_data.append(x)
        report_datetime.append(dt)

    report_avg = calc_average(report_data)

    # PLot the full result of the total query.
    plot_chart("s4_values.jpg", report_datetime, report_data, report_avg)
    # create_json(report_data1440, ion_min, ion_max)