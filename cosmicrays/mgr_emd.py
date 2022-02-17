import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import datetime
import emd
import numpy as np

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def plot_histogram(x, title):
    fig = go.Figure()
    fig.update_layout(title=title)
    for i in range(0, len(x[0])):
        fig.add_trace(go.Histogram(x=x[:, i]))
        # fig.add_trace(go.Scatter(y=x[:,i], mode="lines"))
    fig.show()


def wrapper(datafile, plotname):
    window = 60 * 60 * 6
    nt = int(datafile[len(datafile) - 1])
    st = int(datafile[0])

    print("Start time: ", posix2utc(st, '%Y-%m-%d %H:%M'))
    print("Now time: ", posix2utc(nt, '%Y-%m-%d %H:%M'))

    times = []
    times.append(0)
    for i in range(st, nt):
        times.append(0)

    for item in datafile:
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

    n = np.array(data, dtype='float')

    sample_rate = len(n)
    imf = emd.sift.sift(n)

    # fig = go.Figure(go.Scatter(x=dates, y=imf))
    # fig.show()

    print("data is " + str(len(imf)) + " records long")
    print("Plot finished")


