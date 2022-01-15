from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data):
    fig = go.Figure(go.Scatter(x=dates, y=data))
    fig.update_xaxes(nticks=120, ticks='outside', tickangle=90)
    # fig.update_yaxes(range=[-5000, 5000])
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=600,
                      title="Cosmic Ray Strikes",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.write_image("muon_events.png")
    # fig.show()

def wrapper(data):
    if len(data) > 3:
        # Convert the data to an integer
        d = []
        for item in data:
            i = int(item)
            d.append(i)

        # get the avg interval between timestamps
        t = []
        for i in range(1, len(d)):
            x = d[i] - d[i-1]
            if x > 10000:
                x = 0
            t.append(x)

        period_avg = mean(t)
        d.pop(0)
        x_axis = []
        for item in d:
            u = posix2utc(item, '%Y-%m-%d %H:%M')
            x_axis.append(u)

        y_axis = []
        for item in t:
            v = item - period_avg
            y_axis.append(v)

        plot(x_axis, y_axis)




