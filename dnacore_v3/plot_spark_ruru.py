import matplotlib.pyplot as plt
import PIL
from datetime import datetime

minvalue = 0
maxvalue = 3
data = []
hours = []
title = "Ruru Observatory"
savefile = "spark_ruru.png"

tempdata = []

def convert_datetime_to_hour(datetimestring):
    timeformat = "%Y-%m-%d %H:%M:%S"
    dateobject = datetime.strptime(datetimestring, timeformat)
    hr = datetime.strftime(dateobject, "%H")
    return hr

with open("Ruru_Obs_1hrdx.csv", "r") as f:
    for line in f:
        dd = []
        d = line.strip("\n")
        d = d.split(",")
        hr = d[0]
        da = float(d[1])
        dd.append(da)
        hr = convert_datetime_to_hour(hr)
        hours.append(hr)
        data.append(dd)
print(data)

# draw the heatmap
# plt.figure(figsize=(5,1))
fig, ax = plt.subplots(figsize=(3,7))
ax.set_yticks(range(len(hours)))
ax.set_yticklabels(hours)
ax.set_xticks([])
ax.set_ylabel("UTC Hour")
ax.set_title(title)

b = ax.imshow(data, cmap='viridis', interpolation="hanning", vmin=minvalue, vmax=maxvalue, extent=(0,5,0,24))
cbar = ax.figure.colorbar(b, ax=ax)
cbar.ax.set_ylabel("x background level")

# plt.colorbar(b)
fig.tight_layout()
plt.savefig(savefile)
plt.close('all')