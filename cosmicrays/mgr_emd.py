import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import matplotlib.pyplot as plt
import datetime
import emd
import numpy as np
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def plot_data(imf, dates, filename):
    rownum = imf.shape[1]
    fig = make_subplots(rows=rownum, cols=1)

    iters = len(imf[0])
    for i in range(0, iters):
        fig.add_trace(go.Scatter(x=dates, y=imf[:, i], mode="lines"), row=i, col=1)
    # fig.update_layout(height=500)
    fig.show()


def wrapper(emd_data, dates, plotname):
    n = np.array(emd_data, dtype='float')

    sample_rate = len(n)
    imf = emd.sift.iterated_mask_sift(n)

    print("Intrinsic mode function parameters: ", imf.shape)
    plot_data(imf, dates, plotname)



