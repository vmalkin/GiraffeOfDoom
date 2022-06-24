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

    # create an empty arrag of zeros based on length of time
    hits = []
    hits.append(0)
    for i in range(st, nt):
        hits.append(0)
    print("Length of temp array: ", len(hits))

    # Populate indices that have a date with a one.
    for d in data:
        index = int(d) - st
        hits[index] = 1

    finaldates = []
    finaldata = []
    holding = []
    for i in range(st, nt):
        index = i - st
        parse_window = window * 2
        holding.append(hits[index])

        if len(holding) > parse_window:
            holding.pop(0)
            temp_data = sum(holding)
            temp_time = i - window
            temp_time = posix2utc(temp_time, '%Y-%m-%d %H:%M')
            finaldates.append(temp_time)
            finaldata.append(temp_data)

    print("Plotting average hits")
    plot(finaldates, finaldata, ticknumber, window_hours)