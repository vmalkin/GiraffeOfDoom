from plotly import graph_objects as go
import datetime
from statistics import mean

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot(dates, data, average):
    clr_grid = '#c7c7c7'
    line_color = "#23007d"
    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker=dict(color=line_color, line=dict(width=1, color=line_color))))
    # fig = go.Figure(go.Scatter(x=dates, y=data, line_color="#23007d", line_width=2))
    fig.add_hline(y=average, line_color="red", line_width=2, annotation_font_color="red",
                  annotation_text="Average", annotation_position="top left")
    fig.update_xaxes(gridcolor=clr_grid, ticks='outside', tickangle=90)
    # fig.update_xaxes(gridcolor=clr_grid, nticks=120, ticks='outside', tickangle=90)
    fig.update_yaxes(gridcolor=clr_grid)
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=600,
                      title="Cosmic Ray Strikes - Time between hits.",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="Seconds between hits",)
    fig.write_image("muon_events.svg")
    # fig.show()

def wrapper(data):
    if len(data) > 3:
        # Convert the data to an integer
        d = []
        for item in data:
            i = int(item)
            d.append(i)

        # get the avg interval between timestamps
        y_axis = []
        for i in range(1, len(d)):
            x = d[i] - d[i-1]
            if x > 10000:
                x = 0
            y_axis.append(x)

        period_avg = mean(y_axis)

        d.pop(0)
        x_axis = []
        for item in d:
            u = posix2utc(item, '%Y-%m-%d %H:%M')
            x_axis.append(u)

        plot(x_axis, y_axis, period_avg)




