import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

minvalue = 0
maxvalue = 3
null_value = 0
hour_label_spacing = 6
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
    hours = []
    # ticks = []
    i = 30
    for line in f:
        d = line.strip("\n")
        d = d.split(",")
        hr = d[0]
        da = float(d[1])
        if da > 0:
            d_hi.append((da))
            d_lo.append(null_value)
        if da <= 0:
            d_hi.append(null_value)
            d_lo.append((da))

        # convert posix stamp to UTC and generate a list of every nth label
        hr = convert_datetime_to_hour(hr)
        # hours.append(hr)
        if i % hour_label_spacing == 0:
            hours.append(hr)
            # ticks.append(i)
        else:
            hours.append("")
            # ticks.append(i)
        i = i + 1

fig, ax = plt.subplots(figsize=(4, 7))

ax.set_xticks([-9,-9,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9])
ax.set_ylabel("UTC Hour")
ax.set_xlabel("Bz - nT")
ax.set_title(title)
# ax.bar(x=ticks, height=d_hi, color='#509050')
# ax.bar(x=ticks, height=d_lo, color='red')

ax.barh(y=hours, width=d_hi, color='#509050')
ax.barh(y=hours, width=d_lo, color='red')
plt.grid(color='#95a5a6', linestyle='-', linewidth=1, axis='x', alpha=0.7)
plt.grid(color='#95a5a6', linestyle='-', linewidth=1, axis='y', alpha=0.7)

fig.tight_layout()
plt.yticks(ticks=hours, labels=hours, rotation=0)
# fig.subplots_adjust(bottom=0.17)

# plt.show()
plt.savefig(savefile)
plt.close('all')