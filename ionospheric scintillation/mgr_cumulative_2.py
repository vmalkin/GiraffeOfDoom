import constants as k
import sqlite3
import datetime
import time
import plotly.graph_objects as go
from statistics import mean, stdev
import json

sat_database = "gps_satellites.db"
nullvalue = "none"

class Bin:
    def __init__(self, posixtime):
        self.time = posixtime

        # a count of s4 spikes
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


def plot_chart(filename, dates, data, ion_min, ion_max, ion_average):
    green = "rgba(0, 100, 0, 0.7)"
    red = "rgba(150, 0, 0, 0.7)"
    blue = "rgba(0, 0, 150, 0.7)"
    y_min = min(data) - 2
    y_max = max(data) + 2

    savefile = k.dir_images + "//" + filename
    plotdata = go.Scatter(x=dates, y=data, mode="lines")
    fig = go.Figure(plotdata)
    fig.update_xaxes(nticks=30, tickangle=45)
    fig.update_yaxes(range=[y_min ,y_max] )
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(width=1400, height=600, title="GPS Noise Spikes. Cumulative Total.",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="Count S4 events > 40%",
                      plot_bgcolor="#e0e0e0")
    fig.update_traces(line=dict(width=3, color="rgba(10,10,10,1)"))
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    # manually edit min max markers
    fig.add_hline(y=ion_max, line_color=red, line_width=6, annotation_text="Noisy Ionosphere",
                  annotation_font_color=red, annotation_font_size=20, annotation_position="top left")

    fig.add_hline(y=ion_average, line_color=green, line_width=6, annotation_text="Average",
                  annotation_font_color=green, annotation_font_size=20, annotation_position="top left")

    fig.add_hline(y=ion_min, line_color=blue, line_width=6, annotation_text="Quiet Ionosphere",
                  annotation_font_color=blue, annotation_font_size=20, annotation_position="bottom left")


    fig.write_image(file=savefile, format='jpg')
    # fig.show()


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


def create_json(report_data, ion_min, ion_max):
    result = "none"
    dtm = int(time.time())

    if len(report_data) > 60:
        dtm = dtm
        dta = report_data[-60:]
        dta = mean(dta)

        if dta < ion_min:
            result = "none"

        if dta > ion_min:
            if dta <= ion_max:
                result = "low"

        if dta > ion_max:
            result = "high"

    i = {"posixtime": dtm, "ionstate": result}
    # print(dta, ion_min, ion_med, ion_max)
    print(i)

    filepath = "ion.json"
    with open(filepath, "w") as j:
        json.dump(i, j)


def wrapper():
    nowtime = int(time.time())
    posix_day = 60*60*24
    starttime = nowtime - (posix_day * 28)  # A Carrington Rotation
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
                binlist[i].data.append(1)  # add a 1-count to the list

    # lists for plotting
    report_data1440 = []
    report_data60 = []
    report_datetime1440 = []
    report_datetime60 = []
    temp1440 = []
    temp60 = []

    # Parse thru the list of bins, each entry in the report data represents a running cumulative total
    # of S4 spikes for the previous 24 hour period.
    for i in range(0, len(binlist)):
        x = binlist[i].sumdata()
        temp1440.append(x)
        temp60.append(x)

        if len(temp60) > 60:
            temp60.pop(0)
            y = sum(temp60)
            report_data60.append(y)
            d = posix2utc(binlist[i].time, '%Y-%m-%d %H:%M')
            report_datetime60.append(d)

        # We've now created a 24hour window of cumulative data, start sliding thru this to create the cumulative output
        if len(temp1440) > 1440:
            temp1440.pop(0)
            y = sum(temp1440)
            report_data1440.append(y)
            d = posix2utc(binlist[i].time, '%Y-%m-%d %H:%M')
            report_datetime1440.append(d)

    ion_average = mean(report_data1440)
    ion_sigma = stdev(report_data1440)
    ion_max = ion_average + (2 * ion_sigma)
    ion_min = ion_average - (2 * ion_sigma)

    # PLot the full result of the total query.
    plot_chart("full_cumulative.jpg", report_datetime1440, report_data1440, ion_min, ion_max, ion_average)

    # to calculate the stats, we use a larger set of data than what we will display
    # so the stats are more stable over the longer term.
    if len(report_data1440) > 1440:
        report_data1440 = report_data1440[-1440:]
        report_datetime1440 = report_datetime1440[-1440:]

    # plot_chart("cumulative.jpg", report_datetime1440, report_data1440, ion_min, ion_max, ion_average)
    # plot_chart("hourly_cumulative.jpg", report_datetime60, report_data60, ion_min, ion_max, ion_average)
    create_json(report_data1440, ion_min, ion_max)