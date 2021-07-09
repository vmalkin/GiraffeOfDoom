"""
This file:
* Creates a json file with the format: {"posixtime": 1625362051, "ionstate": "low"}
based on the current S4 value compared to the mean value for the last carrington rotation.

* displays a 24 hour plot of average S4, average SNR, count of s4 noise over 40%.
"""
import constants as k
import sqlite3
import datetime
import time
from statistics import mean, median
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sat_database = "gps_satellites.db"
nullvalue = "none"


class Bin:
    def __init__(self):
        self.time = nullvalue
        self.s4 = []
        self.snr = []
        self.s4_spikes = [0]

    def get_avg_s4(self):
        if len(self.s4) > 0:
            m =  mean(self.s4)
        else:
            m = nullvalue
        return m

    def get_avg_snr(self):
        if len(self.snr) > 0:
            s = mean(self.snr)
        else:
            s = nullvalue
        return s

    def get_sum_spike(self):
        return sum(self.s4_spikes)

    def get_time(self):
        return self.time


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def query_get_data(start):
    optimum_altitude = 25
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


def calc_median(array):
    temp = []
    half_len = 2

    if len(array) > half_len * 2:
        for i in range(half_len, len(array) - half_len):
            t = []
            u = 0
            for j in range(0 - half_len, half_len):
                if isinstance(array[i + j], (float, int)) is True:
                    t.append(array[i + j])
            if len(t) == 0:
                u = 0
            if len(t) == 1:
                u = sum(t)
            if len(t) > 1:
                u = median(t)
            temp.append(u)
    return temp


def recursive_smooth(array, parameter):
    temp = []
    st_prev = array[0]
    for i in range(1, len(array)):
        st_now = (parameter * array[i]) + ((1 - parameter) * st_prev)
        temp.append(st_now)
        st_prev = st_now
    return temp


def plot_chart(dt, s4, snr, spikes):
    s4 = calc_median(s4)
    s4 = recursive_smooth(s4, 0.5)
    # snr = calc_median(snr)
    # snr = recursive_smooth(snr, 0.5)

    fig = make_subplots(rows=3, cols=1, subplot_titles=("Average S4 (Scintillation) Index", "Average S/N Ratio - All Visible Satellites", "GPS Noise Spikes per Minute"))

    fig.add_trace(go.Scatter(x=dt, y=s4, mode="lines", name="Avg S4 Index",
                              line=dict(width=2, color="#008000")), row=1, col=1)
    fig.add_trace(go.Scatter(x=dt, y=snr, mode="lines", name="Avg S/N Ratio",
                              line=dict(width=2, color="#800000")), row=2, col=1)
    fig.add_trace(go.Bar(x=dt, y=spikes,
                         name="S4 Noise Spikes above 40%",
                         marker=dict(color="black", line=dict(width=2, color="black"))), row=3, col=1)

    fig.update_yaxes(range=[5, 40], title_text="%", row=1, col=1)
    fig.update_yaxes(title_text="dB", row=2, col=1)
    fig.update_yaxes(title_text="Number per Minute", row=3, col=1)

    fig.update_xaxes(nticks=30, tickangle=45, gridcolor='#ffffff')
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=1200, title="Data GPS and GLONASS Constellations")
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    savefile = k.dir_images + "//GPS.jpg"
    fig.write_image(file=savefile, format='jpg')


def wrapper():
    nowtime = int(time.time())
    starttime = nowtime - (60 * 60 * 24)
    binlist = []

    for i in range(0, 1451):
        binlist.append(Bin())

    datalist = query_get_data(starttime)

    for item in datalist:
        i = indexposition(item[1], starttime)
        if i >= 0:
            if i <= 1440:
                t = posix2utc(item[1], '%Y-%m-%d %H:%M')
                binlist[i].time = t
                binlist[i].s4.append(float(item[4]))
                binlist[i].snr.append(float(item[5]))
                if item[4] > 40:
                    if item[2] > 30:
                        binlist[i].s4_spikes.append(1)

    dt = []
    s4 = []
    snr = []
    spikes = []

    for b in binlist:
        dt.append(b.get_time())
        s4.append(b.get_avg_s4())
        snr.append(b.get_avg_snr())
        spikes.append(b.get_sum_spike())

    plot_chart(dt, s4, snr, spikes)

