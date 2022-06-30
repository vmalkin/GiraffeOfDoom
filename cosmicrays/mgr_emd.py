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
        fig.add_trace(go.Scatter(x=dates, y=imf[:, i], mode="lines"), row=i+1, col=1)
    fig.update_layout(height=1600, width=1400, title_text="Muon Counts 356 Days - Empirical Mode Decomposition")
    # fig.show()
    fig.write_html("emd.html")
    fig.write_image(filename)

def wrapper(emd_data, dates, plotname):
    n = np.array(emd_data, dtype='float')

    sample_rate = len(n)
    # imf = emd.sift.iterated_mask_sift(n)
    imf = emd.sift.sift(n, max_imfs=7)

    print("Intrinsic mode function parameters: ", imf.shape)
    plot_data(imf, dates, plotname)



