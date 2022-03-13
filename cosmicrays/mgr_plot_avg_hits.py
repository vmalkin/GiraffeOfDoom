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
    # fig.show()

def wrapper(data, window_hours):
    window = 60 * 60 * window_hours

    nt = int(data[len(data) - 1])
    st = int(data[0])
    ticknumber = int((nt - st) / (3600 * 6))

    if ticknumber <= 0:
        ticknumber = 1

    times = []
    for i in range(st, nt):
        times.append(i)

    finaldates = []
    finaldata = []
    for i in range(st + window, nt - window):
        slice_start = i - window
        slice_end = i + window
        compare_set = set()
        for j in range(slice_start, slice_end):
            compare_set.add(j)
        d = len(compare_set.intersection(data))
        print(compare_set.intersection(data))
        finaldata.append(d)
        finaldates.append(posix2utc(i, '%Y-%m-%d %H:%M'))

    plot(finaldates, finaldata, ticknumber, window_hours)


