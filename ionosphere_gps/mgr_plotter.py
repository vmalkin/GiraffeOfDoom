import math
from plotly import graph_objects as go
import random
import standard_stuff

random.seed()


def basicplot(plotdata):
    # ('gp01', now + 1, 20, 100, 34)
    print('Perform plot')
    data = go.Scattergl(mode='markers')
    fig = go.Figure(data)
    fig.update_layout(width=3600, height=900, plot_bgcolor='black')

    timedata = []
    snr_data = []

    for item in plotdata:
        pxtime = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M')
        snr = item[1]
        timedata.append(pxtime)
        snr_data.append(snr)

    fig.add_scattergl(x=timedata, y=snr_data, mode='markers', marker=dict(color='#ffff00', size=5))
    fig.write_image('basicplot.png')

def polarplot_paths(plotdata):
    fig = go.Figure()
    fig.update_layout(width=1200, height=1200, showlegend=False)
    fig.update_layout(polar=dict(angularaxis=dict(rotation=-90, direction="counterclockwise", gridcolor="#505050", color="#000000")))
    fig.update_polars(radialaxis_tickangle=270, radialaxis_angle=270,
                      radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050", range=[0, 90]),
                      bgcolor="#101010")
    rad_data = []
    theta_data = []
    snr_data = []
    label_old = plotdata[0][0]
    for i in range(0, len(plotdata)):
        label = plotdata[i][0]
        r = plotdata[i][2]
        th = plotdata[i][3]
        snr = plotdata[i][4]
        rad_data.append(r)
        theta_data.append(th)
        snr_data.append(snr)
        if label_old != label:

            clr = '#' + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))
            # fig.add_scatterpolargl(r=rad_data, theta=theta_data, mode='markers', marker=dict(color=clr, size=snr_data))
            fig.add_scatterpolargl(r=rad_data, theta=theta_data, mode='markers', marker=dict(color=clr, size=4))
            fig.add_scatterpolargl(r=[r], theta=[th], mode='markers+text', text=label_old,
                                   textfont=dict(color="#ffffff"),marker=dict(color='#ffffff', size=1))
            label_old = label
            rad_data = []
            theta_data = []
    fig.write_image('polar_tracks.png')

