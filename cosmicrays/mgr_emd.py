import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

    print(len(dates), len(data))

    n = np.array(data, dtype='float')

    sample_rate = len(n)
    imf = emd.sift.sift(n)
    print(imf.shape)
    IP, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'hilbert')
    # Define frequency range (low_freq, high_freq, nsteps, spacing)
    freq_range = (1, 20, 10, 'linear')
    f, hht = emd.spectra.hilberthuang(IF, IA, freq_range, sum_time=False)

    fig = plt.figure(figsize=(10, 6))
    emd.plotting.plot_imfs(imf, scale_y=True, cmap=True, fig=fig)
    fig.show()

    # fig = plt.figure(figsize=(10, 6))
    # emd.plotting.plot_hilberthuang(hht, len(dates), f,
    #                                time_lims=(2, 4), freq_lims=(0.1, 15),
    #                                fig=fig, log_y=True)


    print("data is " + str(len(imf)) + " records long")

    # # Create the plotly subsplots
    # fig = make_subplots(rows=len(imf[0])+1, cols=1)
    # fig.update_xaxes(nticks=24, tickangle=45)
    # fig.add_trace(go.Scatter(x=dates, y=data, mode="lines", line=dict(width=2, color="#ff0000")), row=1, col=1)
    # for i in range(0, len(imf[0])):
    #     data = imf[:, i]
    #     r = i+2
    #     # fig.add_trace(go.Scatter(x=dt, y=data, mode="lines", line=dict(width=2, color="#000000")), row=r, col=1)
    #     fig.add_trace(go.Scatter(x=dates, y=data, mode="lines", line=dict(width=1)), row=r, col=1)
    # title = "Instrinsic Mode functions - " + plotname
    # fig.update_layout(height=1000, width=1000, title_text=title)
    # # fig.show()
    # filename = "imd_" + plotname + ".svg"
    # fig.write_image(file=filename, format="svg")
    print("Plot finished")


