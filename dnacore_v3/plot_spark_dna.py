import matplotlib.pyplot as plt
from datetime import datetime

minvalue = 0
maxvalue = 3
data = []
hours = []
title = "Dunedin Aurora"
savefile = "spark_dna.png"

tempdata = []

def convert_datetime_to_hour(datetimestring):
    timeformat = "%Y-%m-%d %H:%M:%S"
    dateobject = datetime.strptime(datetimestring, timeformat)
    hr = datetime.strftime(dateobject, "%H")
    return hr

with open("ruruobservatory.org.nz/shortdiffs.csv", "r") as f:
    dd = []
    for line in f:
        d = line.strip("\n")
        d = d.split(",")
        hr = d[0]
        da = float(d[1])
        dd.append(da)
        hr = convert_datetime_to_hour(hr)
        hours.append(hr)
    data.append(dd)


# draw the heatmap
# plt.figure(figsize=(5,1))
fig, ax = plt.subplots(figsize=(5,1))
ax.set_xticks(range(len(hours)))
ax.set_xticklabels(hours)
ax.set_yticks([])
ax.set_title(title)
ax.imshow(data, cmap='viridis', interpolation="hanning", vmin=minvalue, vmax=maxvalue)
fig.tight_layout()
plt.savefig(savefile)
plt.close('all')