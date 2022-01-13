from plotly import graph_objects as go
import datetime

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data):
    pass

def wrapper(data, nowtime):
    starttime = nowtime - (86400 * 1)

    dates = []
    events = []
    for i in range(starttime, nowtime):
        dates.append(posix2utc(i, '%Y-%m-%d %H:%M'))
        if data.count(i) == 1:
            d = 1
        else:
            d = 0
        events.append(d)

    plot(dates, events)

