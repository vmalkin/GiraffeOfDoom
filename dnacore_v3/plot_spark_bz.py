import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

minvalue = 0
maxvalue = 3
null_value = ""
hours = []
title = "IMF Bz"
savefile = "bz.png"

tempdata = []

def convert_datetime_to_hour(datetimestring):
    timeformat = "%Y-%m-%d %H:%M:%S"
    dateobject = datetime.strptime(datetimestring, timeformat)
    hr = datetime.strftime(dateobject, "%H:%M")
    return hr

with open("Geomag_Bz_spark.csv", "r") as f:
    d_hi = []
    d_lo = []
    for line in f:
        d = line.strip("\n")
        d = d.split(",")
        hr = d[0]
        da = float(d[1])
        if da > 0:
            d_hi.append(str(da))
            d_lo.append(null_value)
        if da <= 0:
            d_hi.append(null_value)
            d_lo.append(str(da))
        hr = convert_datetime_to_hour(hr)
        hours.append(hr)

# draw the heatmap

# fig, ax = plt.subplots(figsize=(10,3))
fig, ax = plt.subplots()
ax.set_xticks(range(len(hours)))

tick_space = 1
ax.set_xticklabels(hours)
# ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_space))

ax.set_yticks([-9,-9,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9])
ax.set_xlabel("UTC Hour")
ax.set_title(title)
ax.bar(x=hours, height=d_hi, color='black')
# ax.bar(x=hours, height=d_lo, color='red')
plt.grid(color='#95a5a6', linestyle='-', linewidth=1, axis='y', alpha=0.7)

# fig.tight_layout()
plt.xticks(rotation=90)

plt.show()
# plt.savefig(savefile)
plt.close('all')