from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data, ticknumber):
    fig = go.Figure(go.Scatter(x=dates, y=data, line=dict(width=2, color='#340059')))
    fig.update_xaxes(nticks=ticknumber, ticks='outside',
                     tickangle=45, tickformat="%b %d, %H:%M")
    # fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=400,
                      title="Cosmic Ray Strikes - Cumulative 6 hourly rate",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.write_image("muon_hit_count.jpg")
    # fig.show()

def wrapper(data):
    window = 60 * 60 * 6
    nt = int(data[len(data) - 1])
    st = int(data[0])
    ticknumber = int((nt - st) / (3600 * 6))

    if ticknumber <= 0:
        ticknumber = 1

    # dates = []
    # events = []
    # for item in data:
    #     dates.append(posix2utc(item, '%Y-%m-%d %H:%M'))
    #     events.append(1)

    times = []
    times.append(0)
    for i in range(st, nt):
        times.append(0)

    for item in data:
        index = int(item) - st
        times[index] = 1

    dates = []
    data = []
    data_subset = []
    for i in range(st, nt):
        index = int(i) - st
        data_subset.append(times[index])
        if i > (st + window):
            da = sum(data_subset)
            dt = posix2utc(i, '%Y-%m-%d %H:%M')
            dates.append(dt)
            data.append(da)
            data_subset.pop(0)

    plot(dates, data, ticknumber)


