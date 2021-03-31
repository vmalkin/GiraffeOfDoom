import plotly.graph_objects as go
from plotly.subplots import make_subplots
import emd
import numpy as np

a = []
dt = []
# with open("2021-03-20.csv", "r") as f:
with open("Geomag_Bz.csv", "r") as f:
# with open("Ruru_Obs//2021-03-26.csv", "r") as f:
# with open("ruru_obs_dxdt.csv", "r") as f:
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

print("data is " + str(len(imf)) + " records long")

data = go.Scatter(y=a, mode="lines")
fig = go.Figure(data)
fig.show()

for i in range(0, len(imf[0])):
    data = imf[:,i]
    data = go.Scatter(y=data, mode="lines")
    fig = go.Figure(data)
    fig.show()
# imf1 = my_get_next_imf(n)
