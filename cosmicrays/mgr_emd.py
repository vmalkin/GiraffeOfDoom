import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import matplotlib.pyplot as plt
import datetime
import emd
import numpy as np
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def plot_data(dates, imf, title):
    width = len(imf[0])
    for i in range(0, width):
        data = go.Scatter(x=dates, y=imf[:, i], mode="lines")
        fig = go.Figure(data)
        fig.update_layout(height=500)
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

    # --------------------------------------------
    seconds = 20 * 60
    newdata = []
    for i in range(seconds, len(data) - seconds):
        temp = []
        for j in range(0 - seconds, seconds):
            temp.append(data[i + j])
        d = round(mean(temp), 3)
        newdata.append(d)
    dates = dates[seconds:]
    dates = dates[:-seconds]
    print(len(newdata))
    print(len(dates))
    # --------------------------------------------

    data_dx = []
    for i in range(1, len(data)):
        dx = data[i] - data[i - 1]
        data_dx.append(dx)
    dates.pop(0)

    n = np.array(data_dx, dtype='float')

    sample_rate = len(n)
    imf = emd.sift.sift(n)
    print("Intrinsic mode function parameters: ", imf.shape)

    # emd.plotting.plot_imfs(imf[:sample_rate, :], cmap=True, scale_y=True)
    # IP, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'hilbert')
    plot_data(dates, imf, plotname)


    print("data is " + str(len(imf)) + " records long")
    print("Plot finished")


