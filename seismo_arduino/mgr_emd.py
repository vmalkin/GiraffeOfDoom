import time
import numpy as np
import emd
import matplotlib.pyplot as plt

ink_colour = ["#7a3f16", "green", "red", "#ffffff"]
plotstyle = 'bmh'


def plot_data(imf, dates, filename):
    plt.style.use(plotstyle)
    rownum = imf.shape[1]
    plot_height = rownum * 300
    # fig, ax = plt.subplots(nrows=len(imf[0]), layout="constrained", figsize=(16, 8), dpi=140)
    fig, ax = plt.subplots(nrows=len(imf[0]), layout="constrained", figsize=(14, 25), dpi=140)
    title = "Empirical Mode Decomposion - Tilt data. "
    # title = title + "<i>Updated " + posix2utc(time.time(), '%Y-%m-%d %H:%M') + "</i>"

    iters = len(imf[0])
    for i in range(0, iters):
        ax[i].plot(dates, imf[:, i], c=ink_colour[0], linewidth=1)
        # fig.add_trace(go.Scatter(x=dates, y=imf[:, i], mode="lines", line=dict(color=pencolour, width=2)),
        #               row=i+1, col=1)

    savefile = filename
    plt.savefig(savefile)
    plt.close()


def wrapper(wrapped_data, savefile):
    dt_dates = wrapped_data[0]
    dt_readings = wrapped_data[1]
    # for item in readings:
    #     date = posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
    #     dt_dates.append(date)
    #     reading = item[1]
    #     dt_readings.append(reading)

    print(len(dt_dates), len(dt_readings))
    nn = np.array(dt_readings, dtype='float')

    # imf = emd.sift.iterated_mask_sift(n)
    # imf = emd.sift.complete_ensemble_sift(nn)
    imf = emd.sift.sift(nn)

    plot_data(imf, dt_dates, savefile)



