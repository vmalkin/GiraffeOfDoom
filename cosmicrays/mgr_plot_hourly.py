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
                      title="7 Day Cosmic Ray Strikes - Hourly. " + str(hrs) + " hourly rate",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    # fig.write_image("muon_hourly.jpg")
    fig.show()

def wrapper(data):
    hrs = 6
    window = 60 * 60 * hrs

    nt = int(data[len(data) - 1])
    st = int(data[0])

    ticknumber = int((nt - st) / (3600 * 6))
    if ticknumber <= 0:
        ticknumber = 1

    # Create a list the size of all posix times in the interval st - nt
    # set the default value to zero
    events = []
    events.append(0)
    for i in range(st, nt):
        events.append(0)

    # Scan thru the data. for each date that matches, set the date to one
    for item in data:
        index = int(item) - st
        events[index] = 1

    # Calculate the number of events for each time interval.
    eventcounts = []
    eventdates = []
    bucket = []
    for i in range(st, nt):
        index = int(i) - st

        print(index, len(data))

        # dt = int(data[index])
        # bucket.append(dt)
    #     if index % window == 0:
    #         print("calculating bucket")
    #         value = sum(bucket)
    #         eventcounts.append(value)
    #         eventdates.append(i)
    #         bucket = []
    # plot(eventdates, eventcounts, ticknumber, hrs)


