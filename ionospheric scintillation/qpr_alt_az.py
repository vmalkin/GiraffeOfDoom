"""
To create simple scatterplot of S4 data_s4
dependencies include Plotly, Kaleido, Pandas
"""
import datetime
import plotly.graph_objects as go
import constants as k
import time

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


def plot_polar(alt, az, s4):
    savefile = k.imagesdir + "//polar.jpg"
    data = go.Scatterpolar(r=alt, theta=az, mode='markers')
    timenow = posix2utc(time.time())
    plottitle = "Ionospheric disturbance. " + timenow + " UTC. http://DunedinAurora.NZ"
    fig = go.Figure(data)

    fig.update_layout(width=1200, height=1200, title=plottitle)
    fig.update_layout(font=dict(size=22), title_font_size=22)
    fig.update_traces(marker=dict(size=s4, color="rgba(255,0,0,1)", line=dict(width=1, color="rgba(255,255,0,1)")))

    # Zone of local noise
    rval = (0,30,30,30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30 ,30, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0)
    thval = (350,350,360,10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120 ,130, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 360, 350)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, fill="toself"))
    fig.add_annotation(x=0.8, y=0.75, text="Local Noise Zone", bordercolor="#c7c7c7", borderwidth=2, borderpad=4, bgcolor="#ff7f0e")

    fig.update_layout(polar=dict(angularaxis=dict(rotation=90, direction="clockwise", color="#000000")), showlegend=False)
    fig.update_polars(radialaxis=dict(autorange="reversed", color="#f0f0f0"), bgcolor="#101010")



    fig.write_image(file=savefile, format='jpg')
    # fig.show()


# def plot_scatterplot(alt, az, s4):
#     savefile = k.imagesdir + "//altaz.jpg"
#     data = go.Scatter(x=az, y=alt, mode='markers')
#     timenow = posix2utc(time.time())
#     plottitle = "Satellite Position - S4. " + timenow + " UTC. http://DunedinAurora.NZ"
#     fig = go.Figure(data)
#     fig.update_yaxes(range=[0, 90], gridcolor='#505050')
#     fig.update_xaxes(range=[0, 360], nticks=45, tickangle=45, gridcolor='#505050')
#     fig.update_layout(width=2000, height=700, title=plottitle, xaxis_title="Azimuth", yaxis_title="Altitude", plot_bgcolor="#101010")
#     fig.update_traces(marker=dict(size=s4, color="rgba(255,0,0,0.2)", line=dict(width=1, color="rgba(255,255,0,0.2)")))
#     fig.write_image(file=savefile, format='jpg')
#     # fig.show()

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    duration_hrs = 1
    t = int(time.time() - (60 * 60 * duration_hrs))
    alt = []
    az = []
    s4 = []

    for item in queryresults:
        if item[1] >= t:
            alt.append(item[2])
            az.append(item[3])

            if item[4] > 100:
                s4.append(100)
            else:
                s4.append(item[4])

    plot_polar(alt, az, s4)
    # plot_scatterplot(alt, az, s4)
