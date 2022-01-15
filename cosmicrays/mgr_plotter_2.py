from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data):
    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker = dict(color='#340059', line=dict(width=0.5, color='#340059'))))
    fig.update_xaxes(nticks=72, ticks='outside', tickangle=90)
    fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=400,
                      title="Cosmic Ray Strikes",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.write_image("muon_events.png")
    # fig.show()

def wrapper(data, nowtime):
    # Convert the data to an integer
    d = []
    for item in data:
        i = int(item)
        d.append(i)

    # get the avg interval between timestamps
    t = []
    for i in range(1, len(d)):
        x = d[i] - d[i-1]
        t.append(x)

    period_avg = mean(t)
    print(len(t), len(data))

    null_value = None
    starttime = nowtime - (86400 * 3)
    dates = []
    events = []
    for i in range(starttime, nowtime):
        dates.append(posix2utc(i, '%Y-%m-%d %H:%M'))
        i = str(i)
        if data.count(i) == 0:
            d = null_value
        else:
            d = 1
        events.append(d)
    plot(dates, events)

