import standard_stuff
import constants as k
import time
from statistics import mean
from plotly import graph_objects as go

data_file = 'output.csv'
lag_minutes = 60

auto_dates = []
auto_data = []

temp_data = []

with open(data_file, 'r') as f:
    for line in f:
        l = line.strip('\n')
        ll = line.split(',')
        d_time = ll[0][:-3]
        d_data = ll[1].strip('\n')
        if d_data != 'Peak':
            d_data = float(d_data)
            d = [d_time, d_data]
            temp_data.append(d)

# Get rid of CSV headings
temp_data.pop(0)

tmp = []
for i in range(1, len(temp_data)):
    time_current = temp_data[i][0]
    time_prev = temp_data[i - 1][0]
    data_current = temp_data[i][1]

    if time_current == time_prev:
        tmp.append(data_current)

    if time_current != time_prev:
        auto_dates.append(time_prev)
        d = round(mean(tmp), 3)
        auto_data.append(d)
        tmp = []

final_auto_correlation = []
for i in range(0, lag_minutes):
    tmp = []
    for j in range(0, len(auto_data)):
        if j + i < len(auto_data):
            d = auto_data[j] - auto_data[j + i]
            tmp.append(d)

    tmp.reverse()
    for k in range(0, i):
        tmp.append(0)
    tmp.reverse()

    final_auto_correlation.append(tmp)

width = k.plot_width
height = k.plot_height
backgroundcolour = k.plot_backgroundcolour
pencolour = k.plot_pencolour
gridcolour = k.plot_gridcolour

title = "Auto-correlation. "
title = title +  "<i>Updated " + standard_stuff.posix2utc(time(), '%Y-%m-%d %H:%M') + "</i>"

plotdata = go.Histogram()
fig = go.Figure(plotdata)
# plotdata = go.Scatter(x=dt_dates, y=dt_detrend, mode="lines", line=dict(color=pencolour, width=2))

for series in final_auto_correlation:
   fig.add_trace(go.Histogram(x=series))

fig.update_layout(width=width, height=height, title=title,
                  xaxis_title="Date/time UTC<br>http://RuruObservatory.org.nz",
                  yaxis_title="Magnetic Field Strength - Arbitrary Values")
fig.update_layout(plot_bgcolor=backgroundcolour, paper_bgcolor=backgroundcolour)
fig.update_layout(showlegend=False,
                  font_family="Courier New")
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour,
                 zeroline=True, zerolinewidth=2, zerolinecolor=gridcolour)
fig.update_xaxes(nticks=12, ticks='outside',
                 tickformat="%b %d<br>%H:%M")
# fig.write_image(savefile_name)
fig.show()







