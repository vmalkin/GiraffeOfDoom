"""
dependencies include Plotly, Kaleido, Pandas
This file creates a polar plot of the alt/az of S4 values over "normal" for the past 24 hours
"""
import datetime
import plotly.graph_objects as go
import constants as k
import time

# Used in legend and chart series
colourdict = {
    0: "#16164e",
    1: "#212170",
    2: "#0b410b",
    3: "#245513",
    4: "#009700",
    5: "#b7770d",
    6: "#f7bc5b",
    7: "#ffffff"
}

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


def plot_polar(alt, az, s4, colours, splat_threshold):
    savefile = k.imagesdir + "//splat.jpg"
    data = go.Scatterpolar(r=alt, theta=az, mode='markers+text')

    event_count = str(len(s4))
    timenow = posix2utc(time.time(), '%H:%M')
    # timestart = time.time() - (60*60)
    # timestart = posix2utc(timestart, '%H:%M')
    date = posix2utc(time.time(), "%Y-%m-%d")
    plottitle = "GPS Noise. " + str(event_count) + " events above S4 =  " + str(splat_threshold) +  "<br>24 Hour plot. " + date +  "<br>" "Updated " + timenow +  " UTC.<br>http://DunedinAurora.NZ"
    fig = go.Figure(data)

    fig.update_layout(width=1500, height=1200, title=plottitle)
    fig.update_layout(font=dict(size=22), title_font_size=22)
    fig.update_layout(legend_title_text="Data Age")
    # default markers
    fig.update_traces(marker=dict(size=s4, color="rgba(0,0,0,0)", line=dict(width=6, color=colours)))
    # fig.update_traces(marker=dict(size=s4, color=colours, line=dict(width=1, color="black")))

    ####################################################### Zone of local noise #####################################################################
    rval = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    thval = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,0)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="none"))

    rval = (40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40)
    thval = (0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,0)
    fig.add_trace(go.Scatterpolar(r=rval, theta=thval, line_color="green", fill="tonext"))

    fig.add_trace(go.Scatterpolar(r=[90], theta=[0], line_color="black"))  # hacky!
    fig.add_annotation(x=0.8, y=0.75, text="Local Noise Zone", bordercolor="#00c700", borderwidth=2, borderpad=4, bgcolor="#20f00e")
    #################################################################################################################################################

    fig.update_layout(polar=dict(angularaxis=dict(rotation=90, direction="clockwise", gridcolor="#505050", color="#000000")), showlegend=False)
    fig.update_polars(radialaxis_tickangle=270, radialaxis_angle=270,
                      radialaxis=dict(autorange="reversed", color="#909090", gridcolor="#505050", range=[0, 90]),
                      bgcolor="#101010")

    fig.add_annotation(x=1, y=0.65, text="Data Age", font=dict(color="#000000", size=28), borderwidth=0, bordercolor="#000000", borderpad=4, bgcolor="#ffffff")
    for i in range(0, len(colourdict)):
        y_location = (0.07 * i) + 0.1
        j = 8 - i
        text = str(j * 3 - 3) + " to " + str(j * 3) + " hrs"
        fig.add_annotation(x=1, y=y_location, text=text, font=dict(color="#000000", size=22), borderwidth=12, bordercolor=colourdict[i], borderpad=6,)

    fig.write_image(file=savefile, format='jpg')

def create_colourway(posixtime):
    #  dictionary for 3hr bins
    epochstart = time.time() - 86400
    index = int((posixtime - epochstart) / 10800)
    clr = colourdict[index]
    return clr

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    # avoid low altitude obstructions. This could be different to the default altitude for multipath.
    splat_altitiude = 40

    # value above which we record an instance of noise.
    splat_threshold = 40
    alt = []
    az = []
    s4 = []
    colours = []

    # Get noise data
    for item in queryresults:
        s_time = item[1]
        s_alt = item[2]
        s_az = item[3]
        s_s4 = item[4]

        if s_s4 > splat_threshold:
            if s_alt > splat_altitiude:
                if s_s4 > 50:
                    s_s4 = 70
                alt.append(s_alt)
                az.append(s_az)
                s4.append(s_s4)
                colours.append(create_colourway(s_time))

    plot_polar(alt, az, s4, colours, splat_threshold)

