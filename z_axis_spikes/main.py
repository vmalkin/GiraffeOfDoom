import datetime
import calendar
import time
import math
import plotly.graph_objects as go

source = "c://temp//test2.csv"
timeformat = "%Y-%m-%d %H:%M:%S"
threshold = 6

def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def utc2posixtime(utcstring):
    d = datetime.datetime.strptime(utcstring, timeformat)
    posixtime = calendar.timegm(d.timetuple())
    return posixtime

def get_data():
    """Gets data from primary source"""
    r = []
    with open(source, "r") as d:
        for line in d:
            line.strip()
            r.append(line)
    return r

def parse_data(data):
    """checks data fits parameters for further calculation. Data must be "datetime, data" Returns parsed data"""
    time_start = time.time() - 86400
    r = []
    data.pop(0)
    for line in data:
        line.strip()
        line = line.split(",")
        dt = line[0]
        posixtime = utc2posixtime(dt)
        data = line[1]
        if posixtime >= time_start:
            dp = str(dt) + "," + str(data)
            r.append(dp)
    return r


def calc_diffs(data):
    """calculates the rate of change"""
    r = []
    for i in range(1, len(data)):
        prev = data[i-1].split(",")
        now = data[i].split(",")
        prev_data = prev[1]
        now_data = now[1]
        now_date = now[0]
        dt = float(now_data) - float(prev_data)
        dp = now_date + "," + str(dt)
        r.append(dp)
    return r


def remove_negatives(data):
    """Gets negative values and removes the sign"""
    r = []
    for item in data:
        item = item.split(",")
        dt = item[0]
        x = float(item[1])
        da = math.sqrt(x * x)
        dp = dt + "," + str(da)
        r.append(dp)
    return  r

def calc_spikes(data):
    """determins if a value is over/under a threshold and substitues a 1/0"""
    r = []
    for item in data:
        item = item.split(",")
        dt = item[0]
        da = float(item[1])
        if da > threshold:
            i = 1
        else:
            i = 0
        dp = dt + "," + str(i)
        r.append(dp)
    return r


def savefile(z_data):
    """Saves out to a CSV file"""
    with open("z_spikes.csv", "w") as f:
        for item in z_data:
            f.write(item + "\n")
    f.close()


def chart(dataarray):
    dates = []
    data = []
    for item in dataarray:
        item = item.split(",")
        dates.append(item[0])
        data.append(item[1])
    d = [go.Bar(x=dates, y=data)]
    fig = go.Figure(data=d)
    fig.update_layout(width=1200, height=300, bargap=0, plot_bgcolor="white", paper_bgcolor="white")
    fig.update_xaxes(gridcolor='red', visible=True)
    fig.update_yaxes(gridcolor='red', visible=True)
    fig.update_traces(marker=dict(color="rgba(0,0,0,1)", line=dict(width=1, color="rgba(0,0,0,1)")))
    fig.show()



if __name__ == "__main__":
    data = get_data()
    if len(data) > 20:
        data = parse_data(data)
        data = calc_diffs(data)
        data = remove_negatives(data)
        data = calc_spikes(data)
        chart(data)
        savefile(data)
    else:
        print("Insufficient data to perform calculations.")