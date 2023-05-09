from plotly import graph_objects as go
import datetime


def filter_avg(gpsdata):
    pass


def data_diffs(data):
    returnarray = []
    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        returnarray.append(diff)
    return returnarray


def posix2utc(posixtime, timeformat):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

# def utc2posix(utcstring, timeformat):
#     utc_time = time.strptime(utcstring, timeformat)
#     epoch_time = timegm(utc_time)
#     return epoch_time
def plot(gpsdata, timestamps, label, pencolour):
    papercolour = "#000000"
    gridcolour = "#303030"
    width = 1500
    height = 500

    data = go.Scatter(x=timestamps, y=gpsdata, mode='lines',
                                     line=dict(color=pencolour, width=1))
    fig =  go.Figure(data)

    title = label
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour, tickangle=50)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#f0f0f0"), title_font_size=18, )
    fig.update_layout(plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    savefile = label + ".jpg"
    fig.write_image(savefile)

def wrapper(db_data, label):
    # ['1683423236', '4552.29376', '17029.07', '2', '10', '1.06', '196.4']
    # posixtime, lat, long, position_fix, num_sats, hdop, alt
    datetimes = []
    latitudes = []
    longitudes = []
    hdop = []
    altitude = []
    for item in db_data:
        dt = posix2utc(item[0], "%Y-%m-%d %H:%M:%S")
        datetimes.append(dt)
        latitudes.append(float(item[1]))
        longitudes.append(float(item[2]))
        hdop.append(float(item[5]))
        altitude.append(float(item[6]))


    l = label + "_latitude"
    plot(latitudes, datetimes, l, "#ffff00")

    l = label + "_longitude"
    plot(longitudes, datetimes, l, "#ffff00")

    l = label + " altitude"
    plot(altitude, datetimes, l, "#ffff00")

    l = label + "_HDOP"
    plot(hdop, datetimes, l, "#ffff00")


    # l = label + "_dlat"
    # latitudes = data_diffs(latitudes)
    # plot(latitudes, datetimes, l, "#00ff00")
    #
    # l = label + "_dlong"
    # longitudes = data_diffs(longitudes)
    # plot(longitudes, datetimes, l, "#00ff00")
    #
    # l = label + "_dalt"
    # altitude = data_diffs(altitude)
    # plot(altitude, datetimes, l, "#00ff00")
    #
    # l = label + "_dHDOP"
    # hdop = data_diffs(hdop)
    # plot(hdop, datetimes, l, "#00ff00")
