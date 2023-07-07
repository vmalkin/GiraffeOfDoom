import time
import secrets
from plotly import graph_objects as go
import datetime
from statistics import mean, stdev, median
import standard_stuff

# one and a half hours is 2700 lots of 2 seconds
readings_per_minute = 60
avg_half_window = int(readings_per_minute * 5)
median_half_window = int(readings_per_minute * 2)


class Day:
    def __init__(self, posixdate):
        self.posixstart = posixdate
        self.lat = self.create_datastore()
        self.long = self.create_datastore()
        self.alt = self.create_datastore()
        self.hdop = self.create_datastore()
        self.plot_null = None

    def create_datastore(self):
        t = []
        for i in range(0, 1440):
            t.append([])
        return t

    def get_avg_mins(self, array):
        returnarray = []
        for item in array:
            if len(item) == 0:
                returnarray.append(self.plot_null)
            else:
                avg = mean(item)
                returnarray.append(avg)
        return returnarray


def plot(gpsdata, timestamps, label, pencolour):
    papercolour = "#d0d0d0"
    gridcolour = "#c0c0c0"
    width = 1500
    height = 550

    data = go.Scatter(x=timestamps, y=gpsdata, mode='lines',
                                     line=dict(color=pencolour, width=1))
    fig =  go.Figure(data)

    title = label
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour, nticks=24, tickangle=50)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#202020"), title_font_size=18, )
    fig.update_layout(plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    savefile = label + ".jpg"
    fig.write_image(savefile)


def wrapper(db_data, label):
    print("*** Plotter starting...")
    # ['1683423236', '4552.29376', '17029.07', '2', '10', '1.06', '196.4']
    # posixtime, lat, long, position_fix, num_sats, hdop, alt
    # Indices of data
    psxtime = 0
    lat = 1
    long = 2
    numsats = 4
    hdop = 6
    alt = 6

    current_day = None
    day_stack = []
    d = Day(0)

    for gpsdata in db_data:
        index_day = standard_stuff.posix2utc(gpsdata[psxtime], "%Y-%m-%d")
        if index_day != current_day:
            current_day = index_day
            day_stack.append(d)
            # set the posix date for the Day object to be the start of the UTC day
            psxstart = standard_stuff.utc2posix(index_day, "%Y-%m-%d")
            d = Day(psxstart)

        else:
            index_minute = int((int(gpsdata[psxtime]) - d.posixstart) / 60)
            d.lat[index_minute].append(float(gpsdata[lat]))
            d.long[index_minute].append(float(gpsdata[long]))
            d.alt[index_minute].append(float(gpsdata[alt]))
            d.hdop[index_minute].append(float(gpsdata[hdop]))
    day_stack.append(d)
    day_stack.pop(0)

    for utcday in day_stack:
        plotdata = utcday.get_avg_mins(utcday.lat)
        title = utcday.posixstart
        plot(plotdata, None, str(title), "#ff0000")



