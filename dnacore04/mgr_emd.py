import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib as plot
import emd
import numpy as np


def plot_histogram(x, title):
    fig = go.Figure()
    fig.update_layout(title=title)
    for i in range(0, len(x[0])):
        fig.add_trace(go.Histogram(x=x[:, i]))
        # fig.add_trace(go.Scatter(y=x[:,i], mode="lines"))
    fig.show()


def wrapper(datafile, plotname):
    a = []
    dt = []
    with open(datafile, "r") as f:
        for line in f:
            # print(line)
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
    IP, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'nht')
    freq_edges, freq_centres = emd.spectra.define_hist_bins(1, 200, 300, 'linear')

    spec_weighted = emd.spectra.hilberthuang_1d(IF, np.ones_like(IA), freq_edges)
    # plot_histogram(IF, plotname)

    hht = emd.spectra.hilberthuang(IF[:, 2, None], IA[:, 2, None], freq_edges, mode='amplitude')
    time_centres = np.arange(201) - .5


    print("data is " + str(len(imf)) + " records long")
    # Create the plotly subsplots
    fig = make_subplots(rows=len(imf[0])+1, cols=1)
    fig.update_xaxes(nticks=24, tickangle=45)
    fig.add_trace(go.Scatter(x=dt, y=a, mode="lines", line=dict(width=2, color="#ff0000")), row=1, col=1)
    for i in range(0, len(imf[0])):
        data = imf[:, i]
        r = i+2
        # fig.add_trace(go.Scatter(x=dt, y=data, mode="lines", line=dict(width=2, color="#000000")), row=r, col=1)
        fig.add_trace(go.Scatter(x=dt, y=data, mode="lines", line=dict(width=1)), row=r, col=1)
    title = "Instrinsic Mode functions - " + plotname
    fig.update_layout(height=2000, width=1600, title_text=title)
    # fig.show()
    filename = "imd_" + plotname + ".svg"
    fig.write_image(file=filename, format="svg")
    print("Plot finished")


# wrapper("bbr_bz.csv", "Bz BBR")
# wrapper("bbr_speed.csv", "SW Speed")
# wrapper("bbr_density.csv", "SW Density")
# wrapper("bbr_ruru_h.csv", "RapidRun")
# wrapper("bbr_ruru_original.csv", "Original")

wrapper("Geomag_Bz.csv", "BZ")
wrapper("GOES_16.csv", "GOES 16")
wrapper("Ruru_Obs.csv", "Ruru")
wrapper("SW_speed.csv", "Solar Wind Speed")
wrapper("SW_Density.csv", "Solar Wind Density")
##wrapper("test.csv", "Frankencoil Broadband")


