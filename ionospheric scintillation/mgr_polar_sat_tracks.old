"""
To create simple scatterplot of S4 data_s4
dependencies include Plotly, Kaleido, Pandas
This code creates polar plot of satellite positions with a trail of the last 24 hour
"""
import datetime
import plotly.graph_objects as go
import constants as k
import time
import os

timelapsesavefolder = k.dir_images + "//timelapse"
class SatelliteLabel():
    def __init__(self):
        self.id = None
        self.posixtime = None
        self.alt = None
        self.az = None

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


def plot_polar(alt, az, label_alt, label_az, label_text):
    savefile = k.dir_images + "//" + k.sensor + "_24hr_tracks.jpg"
    data = go.Scatterpolar(r=alt, theta=az, mode='markers+text')

    # data = go.Scatterpolar(r=alt, theta=az, text=id, mode='markers')
    timenow = posix2utc(time.time(), '%H:%M')
    timestart = time.time() - (60*60)
    timestart = posix2utc(timestart, '%H:%M')
    date = posix2utc(time.time(), "%Y-%m-%d")
    plottitle = "GPS tracks. " + k.sensor + " " + date +  " <br>Last 24 Hours. Plotted at " + timenow +  " UTC.<br>http://DunedinAurora.NZ"
    fig = go.Figure(data)

    fig.update_layout(width=1200, height=1200, title=plottitle)
    fig.update_layout(font=dict(size=22), title_font_size=22)
    # default markers
    # fig.update_traces(marker=dict(size=s4, color="rgba(0,155,200,1)", line=dict(width=1, color="rgba(255,255,255,1)")))
    fig.update_traces(marker=dict(size=3, color="rgba(255,100,0,1)", line=dict(width=1, color="rgba(255,255,255,1)")))


    ####################################################### Satellite ID markers  ###################################################################
    fig.add_trace(go.Scatterpolar(
        r=label_alt, theta=label_az, mode='markers+text', marker_symbol="circle",
        text=label_text, textposition="top center", textfont=dict(size=16, color="#ffffff"),
        marker=dict(size=15, color="#ffffff")
        ))
    #################################################################################################################################################


    ####################################################### Zone of local noise #####################################################################
    rval = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    thval = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="none"))

    rval = (20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20)
    thval = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="tonext"))

    fig.add_trace(go.Scatterpolar(r=[90], theta=[0], line_color="black"))  # hacky!
    fig.add_annotation(x=0.18, y=0.58, text="Trees", bordercolor="#00c700", borderwidth=2, borderpad=4,
                       bgcolor="#20f00e")
    fig.add_annotation(x=0.27, y=0.8, text="Trees", bordercolor="#00c700", borderwidth=2, borderpad=4,
                       bgcolor="#20f00e")
    fig.add_annotation(x=0.27, y=0.17, text="Pine Tree", bordercolor="#00c700", borderwidth=2, borderpad=4,
                       bgcolor="#20f00e")
    #################################################################################################################################################

    fig.update_layout(polar=dict(angularaxis=dict(rotation=90, direction="clockwise", gridcolor="#505050", color="#000000")), showlegend=False)
    fig.update_polars(radialaxis_tickangle=270, radialaxis_angle=270,
                      radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050", range=[0, 90]),
                      bgcolor="#101010")

    fig.write_image(file=savefile, format='jpg')



# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    if os.path.isdir(timelapsesavefolder) is False:
        os.makedirs(timelapsesavefolder)

    duration_hrs = 24
    snr_threshold = 0
    t = int(time.time() - (60 * 60 * duration_hrs))
    alt = []
    az = []
    labellist = {}

    # Get noise data
    for item in queryresults:
        s_satname = item[0]
        sattime = item[1]
        s_alt = item[2]
        s_az = item[3]
        snr = item[4]

        if sattime >= t:
            if snr >= snr_threshold:
                alt.append(s_alt)
                az.append(s_az)
                # update the most recent sat data for labels
            labellist[s_satname] = [s_alt, s_az]

    labelalt = []
    labelaz = []
    labeltext = []
    # parse out label data
    for item in labellist:
        labeltext.append(item)
        labelalt.append(labellist[item][0])
        labelaz.append(labellist[item][1])

    plot_polar(alt, az, labelalt, labelaz, labeltext)
    # plot_scatterplot(alt, az, s4)
