from plotly import graph_objects as go
import random

random.seed()


def basicplot(plotdata):
    # ('gp01', now + 1, 20, 100, 34)
    print('Perform plot')
    data = go.Scattergl(mode='markers')
    fig = go.Figure(data)
    fig.update_layout(width=3600, height=900)

    alt_data = []
    az_data = []
    label_old = plotdata[0][0]
    for item in plotdata:
        label = item[0]
        alt = item[2]
        az = item[3]
        alt_data.append(alt)
        az_data.append(az)
        if label_old != label:
            clr = '#' + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))
            fig.add_scattergl(x=az_data, y=alt_data, mode='markers', marker=dict(color=clr, size=10))
            label_old = label
            alt_data = []
            az_data = []
    fig.write_image('basicplot.png')

