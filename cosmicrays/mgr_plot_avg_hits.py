from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data, ticknumber, hrs):
    fig = go.Figure(go.Scatter(x=dates, y=data, line=dict(width=2, color='#340059')))
    fig.update_xaxes(nticks=ticknumber, ticks='outside',
                     tickangle=45, tickformat="%b %d, %H:%M")
    # fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=400,
                      title="Muons - Average Hits " + str(hrs) + " hour avg.",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    title = "muons_avg_" + str(hrs) + "_hr.jpg"
    fig.write_image(title)
    fig.show()

def wrapper(data, window_hours):
    window = 60 * 60 * window_hours

    nt = int(data[len(data) - 1])
    st = int(data[0])
    ticknumber = int((nt - st) / (3600 * 6))
    if ticknumber <= 0:
        ticknumber = 1

    # create an empty arrag of zeros based on length of time
    temp = []
    temp.append(0)
    for i in range(st, nt):
        temp.append(0)

    # Populate indices that have a date with a one.
    for d in data:
        index = int(d) - st
        temp[index] = 1

    finaldates = []
    finaldata = []
    for i in range(st + window, nt - window):
        t = 0
        for j in range(0 - window, window):
            t = t + temp[i + j]
        finaldates.append(i)
        finaldata.append(t)

    plot(finaldates, finaldata, ticknumber, window_hours)