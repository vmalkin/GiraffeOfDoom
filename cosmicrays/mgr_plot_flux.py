from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data):
    fig = go.Figure(go.Scatter(x=dates, y=data,
                           marker = dict(color='#340059', line=dict(width=0.5, color='#340059'))))
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    title = "7 Day Cosmic Ray. Variation in hit frequency"
    fig.update_layout(width=1400, height=400,
                      title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.write_image("muon_hit_dxdt.jpg")
    # fig.show()


def calculate_differences(data):
    returndata = []
    for i in range(1, len(data)):
        dx = int(data[i]) - int(data[i - 1])
        returndata.append(dx)
    return returndata


def calculate_residuals(dxdt, average_time):
    returndata = []
    for item in dxdt:
        rs = average_time - item
        returndata.append(rs)
    return returndata


def wrapper(data):
    # calculate the average intervals between readings.
    dxdt = calculate_differences(data)
    average_time = mean(dxdt)

    # calculate the residuals in the dxdt data
    residuals = calculate_residuals(dxdt, average_time)

    dates = []
    data.pop(0)

    for item in data:
        d = posix2utc(item, '%Y-%m-%d %H:%M')
        dates.append(d)

    plot(dates, residuals)
    


