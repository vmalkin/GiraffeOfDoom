import time
import secrets
from plotly import graph_objects as go
import datetime
from statistics import mean, stdev, median
avg_half_window = 90
median_half_window = 90


def get_mean(data):
    returnvalue = None
    if len(data) > 0:
        returnvalue = mean(data)
    return returnvalue

def get_median(data):
    returnvalue = None
    if len(data) > 0:
        returnvalue = median(data)
    return returnvalue

def get_stdev(data):
    returnvalue = None
    if len(data) > 0:
        returnvalue = stdev(data)
    return returnvalue


def filter_avg(gpsdata):
    returndata = []
    temp = []
    oldprogress = 0
    if len(gpsdata) > 2 * avg_half_window:
        for i in range(0, len(gpsdata)):
            progress = round((i / len(gpsdata)), 2)
            if oldprogress == progress:
                pass
            else:
                print("averaging: ", progress)
            oldprogress = progress

            temp.append(gpsdata[i])
            if len(temp) > avg_half_window * 2:
                temp.pop(0)
                dp = mean(temp)
                returndata.append(dp)
    else:
        returndata = gpsdata

    return returndata


def filter_median(gpsdata):
    returndata = []
    temp = []
    if len(gpsdata) > 2 * median_half_window:
        for i in range(0, len(gpsdata)):
            temp.append(gpsdata[i])
            if len(temp) > avg_half_window * 2:
                temp.pop(0)
                dp = median(temp)
                returndata.append(dp)
    else:
        returndata = gpsdata

    return returndata


# def data_diffs(data):
#     returnarray = []
#     for i in range(1, len(data)):
#         diff = data[i] - data[i - 1]
#         returnarray.append(diff)
#     return returnarray


def detrend(data, average):
    # ensure data arrays are same length - data is usually longer.
    diff = len(data) - len(average)
    diff = int(diff / 2)
    data = data[diff:]
    data = data[:-diff]
    returnarray = []
    for i in range(0, len(average)):
        diff = data[i] - average[i]
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
    papercolour = "#d0d0d0"
    gridcolour = "#c0c0c0"
    width = 1500
    height = 550

    data = go.Scatter(x=timestamps, y=gpsdata, mode='lines',
                                     line=dict(color=pencolour, width=1))
    fig =  go.Figure(data)

    title = label
    fig.update_layout(width=width, height=height, title=title,
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour, nticks=24, tickangle=50)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolour)
    fig.update_layout(font=dict(size=16, color="#202020"), title_font_size=18, )
    fig.update_layout(plot_bgcolor=papercolour,
                      paper_bgcolor=papercolour)
    savefile = label + ".jpg"
    fig.write_image(savefile)


def wrapper(db_data, label):
    starttime = time.time()
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

    datetimes = datetimes[avg_half_window:]
    datetimes = datetimes[:-avg_half_window]

    latitudes = filter_median(latitudes)
    avg_latitudes = filter_avg(latitudes)
    dtrend_lats = detrend(latitudes, avg_latitudes)
    l = label + "_latitude"
    plot(dtrend_lats, datetimes, l, "#200050")

    # longitudes = filter_median(longitudes)
    # longitudes = split_data(longitudes)
    # l = label + "_longitude"
    # plot_stacks(avg_series, datetimes, l, "#200050")
    #
    # altitude = filter_median(altitude)
    # altitude = split_data(altitude)
    # l = label + "_altitude"
    # plot_stacks(altitude, datetimes, l, "#200050")
    #
    # hdop = filter_median(hdop)
    # hdop = split_data(hdop)
    # l = label + "_hdop"
    # plot_stacks(hdop, datetimes, l, "#200050")

    # print("Processing GPS latitude data")
    # # latitudes = clean_data(latitudes, 4551, 4553)
    # latitudes = filter_median(latitudes)
    # l = label + "_latitude"
    # plot(latitudes, datetimes, l, "#200050")
    #
    # print("Processing GPS longitude data")
    # # longitudes = clean_data(longitudes, 17027, 17030)
    # longitudes = filter_median(longitudes)
    # l = label + "_longitude"
    # plot(longitudes, datetimes, l, "#200050")
    #
    # print("Processing GPS altitude data")
    # # altitude = clean_data(altitude, 150, 250)
    # altitude = filter_median(altitude)
    # l = label + " altitude"
    # plot(altitude, datetimes, l, "#200050")
    #
    # l = label + "_HDOP"
    # # hdop = clean_data(hdop, 0, 30)
    # hdop = filter_median(hdop)
    # plot(hdop, datetimes, l, "#200050")

    endtime = time.time()
    elapsed = (endtime - starttime) / 60
    print("Processing time: ", elapsed)