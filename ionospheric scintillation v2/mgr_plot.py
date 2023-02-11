# Plotters!
import plotly.graph_objects as go
import datetime
from statistics import mean, median

nullvalue = None

class Bin():
    def __init__(self, posixdate):
        self.data = []
        self.posixdate = posixdate

    def get_data(self):
        returnlist = [nullvalue]
        if len(self.data) > 0:
            returnlist = self.data
        return returnlist

    def get_median(self):
        returnvalue = nullvalue
        if len(self.data) > 0:
            returnvalue = median(self.data)
        return returnvalue

    def get_mean(self):
        returnvalue = nullvalue
        if len(self.data) > 0:
            returnvalue = mean(self.data)
        return returnvalue


def plot_snr(datetimes, satellites, data, comport):
    width = 1500
    height = 600
    papercolour = "#000000"
    gridcolour = "#303030"
    data = go.Scatter(x=datetimes, y=data, mode='markers', name="SNR",
                      marker=dict(
                          color='#ffff00',
                          size=5,
                          opacity=0.5,
                          line=dict(
                              color='#ff0000',
                              width=1
                          ))
                      )
    fig = go.Figure(data)

    # No of satellites
    fig.add_trace(go.Scatter(x=datetimes, y=satellites, name="No of Satellites",
                             line=dict(color='#ff0000', width=3)
                             ))


    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="right",
        x=1,
        y=1.2
    ))
    title = "Signal to Noise Ratio - GPS device on port " + comport
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="SNR - dB",
                      plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    fig.write_image("snr.jpg")


def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot_bin(bindata, comport):
    width = 1500
    height = 600
    papercolour = "#000000"
    gridcolour = "#303030"

    datetimes = []
    data = []
    for item in bindata:
        dt = posix2utc(item.posixdate, "%Y-%m-%d %H:%M")
        datetimes.append(dt)
        data.append(item.get_mean())

    data = go.Scatter(x=datetimes, y=data, mode='lines', name="Mean SNR",
                      marker=dict(
                          color='#ffff00',
                          size=5,
                          opacity=1,
                          line=dict(
                              color='#ff0000',
                              width=1
                          ))
                      )
    fig = go.Figure(data)

    # # No of satellites
    # fig.add_trace(go.Scatter(x=datetimes, y=satellites, name="No of Satellites",
    #                          line=dict(color='#ff0000', width=3)
    #                          ))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="right",
        x=1,
        y=1.2
    ))
    title = "Signal to Noise Ratio - GPS device on port " + comport
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="Mean SNR - dB",
                      plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    fig.write_image("mean_snr.jpg")

def wrapper(raw_data, comport):
    # ['gps23' '1676086324' '6' '51.0655737704918' '90.0' '42.68852459016394']
    # posix time at index 1
    d = raw_data[:, 1]

    d_start = int(min(d))
    d_end = int(max(d))
    binlist = []
    for i in range(d_start, d_end + 60, 60):
        b = Bin(i)
        binlist.append(b)
    # print("Bin list created: ", len(binlist))
    for item in raw_data:
        dt = int(item[1])
        snr = float(item[5])
        index = int((dt - d_start) / 60)
        # print(index, len(binlist))
        binlist[index].data.append(snr)

    dates = []
    for item in d:
        dd = posix2utc(item, '%Y-%m-%d %H:%M')
        dates.append(dd)

    # No of Satellites at index 2
    st = raw_data[:, 2]
    stl = []
    for item in st:
        stl.append(float(item))

    # SNR data at index 5
    s = raw_data[:, 5]
    snr = []
    for item in s:
        snr.append(float(item))

    plot_snr(dates, stl, snr, comport)
    plot_bin(binlist, comport)