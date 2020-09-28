import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

minvalue = 0
maxvalue = 3
null_value = 0
hour_label_spacing = 2
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
    i = 0
    for line in f:
        d = line.strip("\n")
        d = d.split(",")
        hr = d[0]
        da = float(d[1])
        d = []
        if da > 0:
            d_hi.append((da))
            d_lo.append(null_value)
        if da <= 0:
            d_hi.append(null_value)
            d_lo.append((da))
        hr = convert_datetime_to_hour(hr)
        i = i + 1
        if i % hour_label_spacing == 0:
            hours.append(hr)
        else:
            hours.append("")

fig, ax = plt.subplots(figsize=(10, 4))
# ax.set_xticks(range(len(hours)))

ax.set_yticks([-9,-9,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9])
ax.set_xlabel("UTC Hour")
ax.set_title(title)
ax.bar(x=hours, height=d_hi, color='#509050')
ax.bar(x=hours, height=d_lo, color='red')
plt.grid(color='#95a5a6', linestyle='-', linewidth=1, axis='y', alpha=0.7)
fig.tight_layout()
plt.xticks(hours, rotation=90)
# plt.show()
plt.savefig(savefile)
plt.close('all')