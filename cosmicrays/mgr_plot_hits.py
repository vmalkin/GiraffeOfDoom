from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data, ticknumber, count):
    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker = dict(color='#340059', line=dict(width=0.5, color='#340059'))))
    fig.update_xaxes(nticks=ticknumber, ticks='outside',
                     tickangle=45, tickformat="%b %d, %H:%M")
    fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    title = "7 Day Cosmic Ray Strikes. Average interval: " + str(int(count/60)) + " minutes."
    fig.update_layout(width=1400, height=400,
                      title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    # fig.write_image("muon_hits.jpg")
    fig.show()

def wrapper(data):
    nt = int(data[len(data) - 1])
    st = int(data[0])
    ticknumber = int((nt - st) / (3600 * 3))
    if ticknumber <= 0:
        ticknumber = 1

    avg_count = []
    for i in range(1, len(data)):
        t = int(data[i]) - int(data[i-1])
        avg_count.append(t)
    count = int(mean(avg_count))

    dates = []
    events = []
    for item in data:
        dates.append(posix2utc(item, '%Y-%m-%d %H:%M'))
        events.append(1)
    print("Plotting hits")
    plot(dates, events, ticknumber, count)

