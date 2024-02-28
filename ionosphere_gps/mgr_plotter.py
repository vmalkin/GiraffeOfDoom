from plotly import graph_objects as go
from plotly.subplots import make_subplots
import random
import standard_stuff
import constants as k
import os
from statistics import mean

random.seed()
colour_paper = 'lavender'
colour_gridlines = 'beaver'
colour_plotbackground = '#c0d3cf'
colour_pen = '#2f211a'
plotdimensions = [1500, 700]
fontsize_title = 20
fontsize_axis = 15


def snr_azimuth(plotdata):
    label_text = 'SNR vs Azimuth'
    # ('gp01', now + 1, 20, 100, 34)
    data = go.Scattergl(mode='markers')
    fig = go.Figure(data)
    fig.update_layout(width=plotdimensions[0], height=400,
                            paper_bgcolor=colour_paper, plot_bgcolor=colour_plotbackground)
    fig.update_layout(title=label_text)
    az_data = []
    snr_data = []
    for item in plotdata:
        az = item[4]
        snr = item[5]
        az_data.append(az)
        snr_data.append(snr)

    fig.add_scattergl(x=az_data, y=snr_data, mode='markers', marker=dict(color=colour_pen, size=4))
    savefile = k.dir_images + os.sep + 'snr_azimuth.png'
    fig.write_image(savefile)


def polarplot_paths(plotdata):
    fig = go.Figure()
    fig.update_layout(width=plotdimensions[1], height=plotdimensions[1], showlegend=False)
    fig.update_layout(polar=dict(angularaxis=dict(rotation=-90, direction="counterclockwise",
                                                  gridcolor=colour_paper, color="#000000")))
    fig.update_polars(radialaxis_tickangle=270, radialaxis_angle=270,
                      radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050", range=[0, 90]),
                      bgcolor=colour_plotbackground)
    rad_data = []
    theta_data = []
    snr_data = []
    label_old = plotdata[0][0]
    for i in range(0, len(plotdata)):
        label = plotdata[i][0] + plotdata[i][1]
        r = plotdata[i][3]
        if r == '':
            r = None

        th = plotdata[i][4]
        if th == '':
            th = None

        # snr = plotdata[i][5]
        rad_data.append(r)
        theta_data.append(th)
        # snr_data.append(snr)
        if label_old != label:
            # clr = '#' + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))
            clr = colour_pen
            fig.add_scatterpolargl(r=rad_data, theta=theta_data, mode='markers', marker=dict(color=clr, size=4))
            fig.add_scatterpolargl(r=[r], theta=[th], mode='markers+text', text=label_old,
                                   textfont=dict(color="#ff7700", size=25), marker=dict(color='#ff7700', size=1))
            label_old = label
            rad_data = []
            theta_data = []
    savefile = k.dir_images + os.sep + 'basic_tracks.png'
    fig.write_image(savefile)


def avg_snr_time(now, start, query_result):
    # create array of timestamps for plotting
    timestamps = []
    for i in range(start, now + 3):
        t = standard_stuff.posix2utc(i, '%Y-%m-%d %H:%M:%S')
        timestamps.append(t)

    # create array of data for averaging
    data = []
    for i in range(start, now + 3):
        data.append([])

    for d in query_result:
        posixtime = d[2]
        snr = d[5]
        if snr != '':
            index_value = posixtime - start
            data[index_value].append(snr)

    avg_data = []
    for i in range(start, now + 3):
        avg_data.append(0)

    for i in range(0, len(data)):
        if len(data[i]) > 1:
            v = mean(data[i])
            avg_data[i] = v

    diff_data = []
    for i in range(1, len(avg_data)):
        d = avg_data[i] - avg_data[i - 1]
        diff_data.append(d)

    final_data = standard_stuff.filter_average(avg_data, 30)
    diff_data = standard_stuff.filter_average(diff_data, 20)

    fig_snr = go.Figure()
    fig_diffs = go.Figure()

    fig_snr.add_trace(
        go.Scattergl(x=timestamps, y=final_data, mode='markers', marker=dict(color=colour_pen, size=2))
    )
    fig_diffs.add_trace(
        go.Scattergl(x=timestamps, y=diff_data, mode='markers', marker=dict(color=colour_pen, size=2))
    )

    label_text = 'Average SNR'
    fig_snr.update_layout(width=plotdimensions[0], height=plotdimensions[1],
                            paper_bgcolor=colour_paper, plot_bgcolor=colour_plotbackground)
    fig_snr.update_yaxes(range=[15, 40])
    fig_snr.update_layout(title=label_text)
    savefile = k.dir_images + os.sep + 'snr_avg_time.png'
    fig_snr.write_image(savefile)

    label_text = 'SNR Differences'
    fig_diffs.update_layout(width=plotdimensions[0], height=plotdimensions[1],
                            paper_bgcolor=colour_paper, plot_bgcolor=colour_plotbackground)
    fig_diffs.update_yaxes(range=[-0.5, 0.5])
    fig_diffs.update_layout(title=label_text)
    savefile = k.dir_images + os.sep + 'snr_diffs_time.png'
    fig_diffs.write_image(savefile)




