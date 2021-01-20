"""
To create simple scatterplot of S4 data_s4
dependencies include Plotly, Kaleido, Pandas
"""
import datetime
import plotly.graph_objects as go
import constants as k

timeformat = '%Y-%m-%d %H:%M'

def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def save_s4(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write("Datetime UTC, S4 Scintillation Index" + '\n')
            for result in data:
                f.write(result + '\n')
        f.close()
        print("S4 csv"
              " file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")


def plot_scatterplot(xvalues, yvalues):
    savefile = k.imagesdir + "//scatter.jpg"
    data = go.Scatter(x=xvalues, y=yvalues, mode='markers')
    fig = go.Figure(data)
    fig.update_yaxes(range=[1, 20], gridcolor='#505050')
    fig.update_xaxes(nticks=24, tickangle=45, gridcolor='#505050')
    fig.update_layout(width=1700, height=600, title="S4 Indices, GPS & Glonass Constellations", xaxis_title="Date/time UTC", yaxis_title="S4 Index", plot_bgcolor="#101010")
    fig.update_traces(marker=dict(size=5, color="rgba(0,255,255,0.2)", line=dict(width=5, color="rgba(0,200,255,0.1)")))
    # fig.update_traces(marker=dict(size=7, color="rgba(0,255,255,0.2)"))
    fig.write_image(file=savefile, format='jpg')
    # fig.show()

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    datalist = []
    xval = []
    yval = []
    for item in queryresults:
        dt = item[1]
        dt = posix2utc(dt)
        da = item[4]

        xval.append(dt)
        yval.append(da)

        dp = dt + "," + str(da)
        datalist.append(dp)

    save_s4("s4.csv", datalist)
    plot_scatterplot(xval, yval)