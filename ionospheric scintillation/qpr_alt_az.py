"""
To create simple scatterplot of S4 data_s4
dependencies include Plotly, Kaleido, Pandas
"""
import datetime
import plotly.graph_objects as go
import constants as k
import time


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
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


def plot_polar(alt, az, s4, id):
    savefile = k.imagesdir + "//polar.jpg"
    # data = go.Scatterpolar(r=alt, theta=az, text=id, mode='markers+text')
    data = go.Scatterpolar(r=alt, theta=az, text=id, mode='markers')
    timenow = posix2utc(time.time(), '%H:%M')
    timestart = time.time() - (60*60)
    timestart = posix2utc(timestart, '%H:%M')
    date = posix2utc(time.time(), "%Y-%m-%d")
    plottitle = "GPS Signal Noise. " + date +  "<br>" + timestart + " to " + timenow +  " UTC.<br>http://DunedinAurora.NZ"
    fig = go.Figure(data)

    fig.update_layout(width=1200, height=1200, title=plottitle)
    fig.update_layout(font=dict(size=22), title_font_size=22)
    fig.update_traces(marker=dict(size=s4, color="rgba(0,155,200,1)", line=dict(width=1, color="rgba(255,255,255,1)")))

    # Zone of local noise
    rval = (0,30,30,30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30 ,30, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0)
    thval = (350,350,360,10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120 ,130, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 360, 350)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="toself"))
    fig.add_trace(go.Scatterpolar(r=[90], theta=[0], line_color="black"))  # hacky!
    fig.add_annotation(x=0.8, y=0.75, text="Local Noise Zone", bordercolor="#00c700", borderwidth=2, borderpad=4, bgcolor="#20f00e")

    fig.update_layout(polar=dict(angularaxis=dict(rotation=90, direction="clockwise", gridcolor="#505050", color="#000000")), showlegend=False)
    fig.update_polars(radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050"), bgcolor="#101010")
    fig.write_image(file=savefile, format='jpg')
    # fig.show()



# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    duration_hrs = 1
    t = int(time.time() - (60 * 60 * duration_hrs))
    alt = []
    az = []
    s4 = []
    satID = []

    for item in queryresults:
        if item[1] >= t:
            alt.append(item[2])
            az.append(item[3])
            satID.append(item[0])
            if item[4] > 100:
                s4.append(100)
            else:
                s4.append(item[4])

    plot_polar(alt, az, s4, satID)
    # plot_scatterplot(alt, az, s4)
