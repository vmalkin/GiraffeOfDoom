"""
dependencies include Plotly, Kaleido, Pandas
This file creates a polar plot of the alt/az of S4 values over "normal" for the past 24 hours
"""
import datetime
import plotly.graph_objects as go
import time
import constants as k

# Used in legend and chart series
colourdict = {
    0: "#444444",
    1: "#0c2256",
    2: "#1742a4",
    3: "#005900",
    4: "#00c100",
    5: "#b7770d",
    6: "#f7bc5b",
    7: "#ffffff"
}

# timelapsesavefolder = k.imagesdir + "//timelapse"
# class SatelliteLabel():
#     def __init__(self):
#         self.id = None
#         self.posixtime = None
#         self.alt = None
#         self.az = None

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


def plot(ut, da):
    # Here we're using Plotly's grouping function to bin our data into hours. It does this by the time format.
    savefile = k.imagesdir + "//count_s4.jpg"
    data = [go.Bar(x=ut, y=da)]
    layout = go.Layout(barmode="group")
    fig = go.Figure(data=data, layout=layout)
    # fig = go.Figure(data=data)
    fig.update_layout(width=800, height=500, title="S4 count", xaxis_title="Date/time UTC", yaxis_title="Count S4.", plot_bgcolor="#101010", )
    fig.update_yaxes(range=[0, 30], gridcolor='#505050')
    fig.update_xaxes(nticks=24, tickangle=45, gridcolor='#505050')
    fig.write_image(file=savefile, format='jpg')

# def create_colourway(posixtime):
#     #  dictionary for 3hr bins
#     epochstart = time.time() - 86400
#     index = int((posixtime - epochstart) / 10800)
#     clr = colourdict[index]
#     return clr

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    splat_threshold = 40
    splat_altitude = 40
    utc = []
    dat = []
    counter = 0

    # for i in range(0, len(queryresults)-1):
    #     s_time = queryresults[i][1]
    #     s_time_next = queryresults[i+1][1]
    #     s_alt = queryresults[i][2]
    #     s_az = queryresults[i][3]
    #     s_s4 = queryresults[i][4]
    #
    #     if s_time == s_time_next:
    #         if s_s4 > splat_threshold:
    #             if s_alt >= splat_altitude:
    #                 counter = counter + 1
    #     else:
    #         utc.append(str(posix2utc(s_time, '%Y-%m-%d %H')))
    #         dat.append(counter)
    #         counter = 0

    for item in queryresults:
        s_time = item[1]
        s_alt = item[2]
        s_az = item[3]
        s_s4 = item[4]

        if s_s4 > splat_threshold:
            if s_alt >= splat_altitude:
                utc.append(str(posix2utc(s_time, '%Y-%m-%d %H')))
                dat.append(1)
            else:
                utc.append(posix2utc(s_time, '%Y-%m-%d %H'))
                dat.append(0)
    plot(utc, dat)

