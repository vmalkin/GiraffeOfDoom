# Plotters!
import plotly.graph_objects as go
import datetime
def plot_snr(datetimes, satellites, data):
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
    fig.add_trace(go.Scatter(x=datetimes, y=satellites, name="No of Satellites", mode="line",
                             color_continuous_scale=["red", "green", "blue"]))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="right",
        x=1,
        y=1.2
    ))

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )
    fig.update_layout(width=width, height=height, title="Signal to Noise Ratio - GNSS",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="SNR - dB",
                      plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    fig.show()


def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def wrapper(raw_data):
    # posix time at index 1
    d = raw_data[:, 1]
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

    plot_snr(dates, stl, snr)