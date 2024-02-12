from plotly import graph_objects as go
import random

random.seed()


# def basicplot(plotdata):
#     # ('gp01', now + 1, 20, 100, 34)
#     print('Perform plot')
#     data = go.Scattergl(mode='markers')
#     fig = go.Figure(data)
#     fig.update_layout(width=3600, height=900)
#
#     alt_data = []
#     az_data = []
#     label_old = plotdata[0][0]
#     for item in plotdata:
#         label = item[0]
#         alt = item[2]
#         az = item[3]
#         alt_data.append(alt)
#         az_data.append(az)
#         if label_old != label:
#             clr = '#' + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))
#             fig.add_scattergl(x=az_data, y=alt_data, mode='markers', marker=dict(color=clr, size=10))
#             label_old = label
#             alt_data = []
#             az_data = []
#     fig.write_image('basicplot.png')

def polarplot_paths(plotdata):
    fig = go.Figure()
    fig.update_layout(width=900, height=900)
    fig.update_layout(polar=dict(angularaxis=dict(rotation=-90, direction="counterclockwise", gridcolor="#505050", color="#000000")))
    fig.update_polars(radialaxis_tickangle=270, radialaxis_angle=270,
                      radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050", range=[0, 90]),
                      bgcolor="#101010")
    rad_data = []
    theta_data = []
    label_old = plotdata[0][0]
    for item in plotdata:
        label = item[0]
        r = item[2]
        th = item[3]
        rad_data.append(r)
        theta_data.append(th)
        if label_old != label:
            clr = '#' + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))
            fig.add_scatterpolargl(r=rad_data, theta=theta_data, mode='markers', marker=dict(color=clr, size=5))
            label_old = label
            rad_data = []
            theta_data = []
    fig.write_image('polar_tracks.png')