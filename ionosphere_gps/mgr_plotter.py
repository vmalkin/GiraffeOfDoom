from plotly import graph_objects as go
import random
import standard_stuff
import constants as k
import os
from statistics import mean

random.seed()

def snr_azimuth(plotdata):
    print(plotdata[40])
    label_text = 'SNR vs Azimuth'
    # ('gp01', now + 1, 20, 100, 34)
    data = go.Scattergl(mode='markers')
    fig = go.Figure(data)
    fig.update_layout(width=1500, height=500, plot_bgcolor='black')
    fig.update_layout(title=label_text)
    az_data = []
    snr_data = []
    colours = []
    for item in plotdata:
        az = item[4]
        snr = item[5]
        az_data.append(az)
        snr_data.append(snr)

    fig.add_scattergl(x=az_data, y=snr_data, mode='markers', marker=dict(color='orange', size=4))
    savefile = k.dir_images + os.sep + 'snr_azimuth.png'
    fig.write_image(savefile)


def snr_time(plotdata):
    label_text = 'SNR vs Time'
    timedata = []
    snr_data = []

    index_snr = 1
    index_time = 0
    # bin the data
    time_current = plotdata[0][index_time]
    tmp = []

    for i in range(0, len(plotdata) - 1):
        current_snr =  plotdata[i][index_snr]
        if current_snr != '':
            tmp.append(int(current_snr))
        time_next = plotdata[i + 1][index_time]

        if time_next != time_current:
            if len(tmp) > 0:
                avg_snr = mean(tmp)
            else:
                avg_snr = 0
            t = standard_stuff.posix2utc(time_current, '%Y-%m-%d %H:%M')
            timedata.append(t)
            snr_data.append(avg_snr)
            tmp = []
            time_current = time_next

    data = go.Scattergl(x=timedata, y=snr_data, mode='markers', marker=dict(color='#ffff00', size=2))
    fig = go.Figure(data)
    fig.update_layout(width=2000, height=600, plot_bgcolor='black', )
    fig.update_layout(title=label_text)
    savefile = k.dir_images + os.sep + 'snr_time.png'
    fig.write_image(savefile)


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
        label = plotdata[i][0] + plotdata[i][1]
        r = plotdata[i][3]
        th = plotdata[i][4]
        snr = plotdata[i][5]
        rad_data.append(r)
        theta_data.append(th)
        snr_data.append(snr)
        if label_old != label:
            clr = '#' + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))
            # fig.add_scatterpolargl(r=rad_data, theta=theta_data, mode='markers', marker=dict(color=clr, size=snr_data))
            fig.add_scatterpolargl(r=rad_data, theta=theta_data, mode='markers', marker=dict(color=clr, size=4))
            fig.add_scatterpolargl(r=[r], theta=[th], mode='markers+text', text=label_old,
                                   textfont=dict(color="#ff7700", size=25), marker=dict(color='#ff7700', size=1))
            label_old = label
            rad_data = []
            theta_data = []
    savefile = k.dir_images + os.sep + 'basic_tracks.png'
    fig.write_image(savefile)
