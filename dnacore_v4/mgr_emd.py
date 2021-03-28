import plotly.graph_objects as go
from plotly.subplots import make_subplots
import emd
import numpy as np


def plot_histogram(IP, IF, IA):
    fig = go.Figure(go.Scatter(x=IF))
    fig.show()


def wrapper(datafile):
    a = []
    dt = []
    with open(datafile, "r") as f:
        for line in f:
            line = line.split(",")
            d = line[1].strip()
            t = line[0]
            try:
                d = float(str(d))
                a.append(d)
                dt.append(t)
            except:
                pass
    a.pop(0)
    n = np.array(a, dtype='float')

    sample_rate = len(n)
    imf = emd.sift.sift(n)
    emd.plotting.plot_imfs(imf[:sample_rate, :], cmap=True, scale_y=True)
    IP, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'hilbert')
    # plot_histogram(IP, IF, IA)

    print("data is " + str(len(imf)) + " records long")
    # Create the plotly subsplots
    fig = make_subplots(rows=len(imf[0])+1, cols=1)
    fig.update_xaxes(nticks=24, tickangle=45)
    fig.add_trace(go.Scatter(x=dt, y=a, mode="lines", line=dict(width=2, color="#ff0000")), row=1, col=1)

    for i in range(0, len(imf[0])):
        data = imf[:, i]
        r = i+2
        fig.add_trace(go.Scatter(x=dt, y=data, mode="lines", line=dict(width=2, color="#000000")), row=r, col=1)

    fig.update_layout(height=3000, width=1400, title_text="Instrinsic Mode functions")
    fig.show()
    # fig.write_image(file="temp.jpg", format="jpg")
    print("Plot finished")


wrapper("Geomag_Bz.csv")


