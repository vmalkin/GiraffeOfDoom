import matplotlib.pyplot as plt
from datetime import datetime, timedelta

minvalue = 0
maxvalue = 3.2
data = []
hours = []
title = "Dunedin Aurora No 1"
savefile = "spark_ruru.png"

tempdata = []

def convert_datetime_to_hour(datetimestring):
    timeformat = "%Y-%m-%d %H:%M:%S"
    dateobject = datetime.strptime(datetimestring, timeformat) + timedelta(hours=1)
    hr = datetime.strftime(dateobject, "%H:%M")
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
hours.reverse()

# draw the heatmap
fig, ax = plt.subplots(figsize=(3,7))
ax.set_yticks(range(len(hours)))
ax.set_yticklabels(hours)
ax.set_xticks([])
ax.set_ylabel("UTC Hour")
ax.set_title(title)

ax.annotate('Now', xy=(0,0.5), xytext=(0.5, 0.5), color ="white")
ax.annotate('24 hours ago', xy=(0,23), xytext=(0.5, 23), color ="white")

b = ax.imshow(data, cmap='viridis', interpolation="hanning", vmin=minvalue, vmax=maxvalue, extent=(0,5,-0.5,23.5))
# cbar = ax.figure.colorbar(b, ax=ax)
# cbar_labels = ['MIN', 'MAX']
# cbar.set_ticks([minvalue, maxvalue])
# cbar.set_ticklabels(cbar_labels)

fig.tight_layout()
plt.savefig(savefile)
plt.close('all')