import constants as k
import sqlite3
import datetime
import time
import plotly.graph_objects as go

sat_database = "gps_satellites.db"
nullvalue = "none"


class Bin:
    def __init__(self):
        self.time = None
        self.data = [0]

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


def plot_chart(dates, data):
    savefile = k.dir_images + "//cumulative.jpg"
    data = go.Scatter(x=dates, y = data, mode="lines")
    fig = go.Figure(data)
    fig.update_xaxes(nticks=24, tickangle=45)
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(width=1700, height=700, title="Rolling 24hr count GPS noise. s4 > 40. http://DunedinAurora.NZ", xaxis_title="Date/time UTC", yaxis_title="Count S4 events", plot_bgcolor="#e0e0e0")
    fig.update_traces(line=dict(width=5, color="rgba(10,10,10,1)"))
    fig.write_image(file=savefile, format='jpg')


def query_parse(queryresult):
    """
    Filter the raw query result
    """
    s4_min = 40
    s4_max = 100
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


def wrapper():
    nowtime = int(time.time())
    starttime = nowtime - (60 * 60 * 48)
    binlist = []

    for i in range(0, 2880):
        binlist.append(Bin())

    queryresult = query_get_data(starttime)
    parsed_query = query_parse(queryresult)

    for item in parsed_query:
        dt = item[1]
        i = indexposition(dt, starttime)
        if i >=0:
            if i <=2880:
                binlist[i].time = posix2utc(dt, '%Y-%m-%d %H:%M')
                binlist[i].data.append(1)

    report_data = []
    report_datetime = []
    temp = []
    for i in range(0, len(binlist)):
        temp.append(binlist[i].sumdata())
        if len(temp) >= 1440:
            report_datetime.append(binlist[i].time)
            report_data.append(sum(temp))
            temp.pop(0)

    plot_chart(report_datetime, report_data)