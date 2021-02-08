"""
dependencies include Plotly, Kaleido, Pandas
This file creates a polar plot of the alt/az of S4 values over "normal" for the past 24 hours
"""
import datetime
import plotly.graph_objects as go
import constants as k
import time

# timelapsesavefolder = k.imagesdir + "//timelapse"
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


def plot_polar(alt, az, s4, splat_threshold):
    savefile = k.imagesdir + "//splat.jpg"
    data = go.Scatterpolar(r=alt, theta=az, mode='markers+text')

    event_count = str(len(s4))
    timenow = posix2utc(time.time(), '%H:%M')
    timestart = time.time() - (60*60)
    timestart = posix2utc(timestart, '%H:%M')
    date = posix2utc(time.time(), "%Y-%m-%d")
    plottitle = "GPS Noise. " + str(event_count) + " events above S4 =  " + str(splat_threshold) +  "<br>24 Hour plot. " + date +  "<br>" "Updated " + timenow +  " UTC.<br>http://DunedinAurora.NZ"
    fig = go.Figure(data)

    fig.update_layout(width=1200, height=1200, title=plottitle)
    fig.update_layout(font=dict(size=22), title_font_size=22)
    # default markers
    # fig.update_traces(marker=dict(size=s4, color="rgba(0,155,200,1)", line=dict(width=1, color="rgba(255,255,255,1)")))
    fig.update_traces(marker=dict(size=s4, color="darkgoldenrod", line=dict(width=1, color="yellow")))

    ####################################################### Zone of local noise #####################################################################
    rval = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    thval = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,0)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="none"))

    rval = (50,50,50,50,50,50,50,50,35,35,35,35,35,35,35,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,35,35,35)
    thval = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,0)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="tonext"))

    fig.add_trace(go.Scatterpolar(r=[90], theta=[0], line_color="black"))  # hacky!
    fig.add_annotation(x=0.8, y=0.75, text="Local Noise Zone", bordercolor="#00c700", borderwidth=2, borderpad=4, bgcolor="#20f00e")
    #################################################################################################################################################

    fig.update_layout(polar=dict(angularaxis=dict(rotation=90, direction="clockwise", gridcolor="#505050", color="#000000")), showlegend=False)
    fig.update_polars(radialaxis_tickangle=270, radialaxis_angle=270,
                      radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050", range=[0, 90]),
                      bgcolor="#101010")

    fig.write_image(file=savefile, format='jpg')

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    splat_threshold = 40
    alt = []
    az = []
    s4 = []

    # Get noise data
    for item in queryresults:
        s_alt = item[2]
        s_az = item[3]
        s_s4 = item[4]
        if s_s4 > splat_threshold:
            if s_s4 > 50:
                s_s4 = 70
            alt.append(s_alt)
            az.append(s_az)
            s4.append(s_s4)

    plot_polar(alt, az, s4, splat_threshold)

