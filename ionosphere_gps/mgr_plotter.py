from plotly import graph_objects as go

def basicplot(plotdata):
    # ('gp01', now + 1, 20, 100, 34)
    alt = []
    az = []

    for item in plotdata:
        alt.append(item[2])
        az.append(item[3])

    data = go.Scatter(x=az, y=alt, mode='markers')
    fig = go.Figure(data)
    fig.show()

