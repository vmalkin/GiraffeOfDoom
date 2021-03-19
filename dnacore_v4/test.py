"""
dependencies include Plotly, Kaleido, Pandas
"""
import plotly.graph_objects as go
import sqlite3
import logging
import constants as k
from time import time
import datetime
from statistics import mean, median, stdev
import pickle
import os

errorloglevel = logging.WARNING
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
sigma_file = "test.pkl"
station = "Ruru_Obs"
plot_title = "test"
median_sigma = 0
# a 10 min window for averaging readings give the number of readings per minute
halfwindow = 30 * 10

def get_data(station):
    start_time = int(time()) - 86400
    result = db.execute("select station_data.posix_time, station_data.data_value from station_data "
                        "where station_data.station_id = ? and station_data.posix_time > ? order by station_data.posix_time asc", [station, start_time])
    query_result = result.fetchall()
    db.close()
    return query_result


def posix2utc(posixtime, timeformat):
    # timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def plot(hours, data, colours):
    maxaxis = median_sigma * 8
    fig = go.Figure(go.Bar(
        x=data,
        y=hours,
        marker=dict(color=colours),
        orientation='h'
    ))
    fig.update_layout(width=320, height=900, title=plot_title)
    fig.update_layout(font=dict(size=20), margin=dict(l=10, r=20, b=10), yaxis_title="UTC")
    fig.update_xaxes(range=[0, maxaxis], gridcolor='#505050', visible=False)
    # savefile = station + ".jpg"
    savefile = "test.jpg"
    fig.write_image(file=savefile, format='jpg')


def dxdt(querydata):
    # calculate the rate of change, dx/dt
    t = []
    for i in range(1, len(querydata)):
        dt = querydata[i][0]
        d2 = float(querydata[i][1])
        d1 = float(querydata[i-1][1])

        dh = round((d2 - d1), 5)
        dp = (dt, dh)

        t.append(dp)
    return t


def average_out(query_dhdt):
    # smoothes out the dh/dt data
    avg_data = []
    return_data = []

    for i in range(0, len(query_dhdt)):
        temp_data = float(query_dhdt[i][1])
        temp_data = round(temp_data, 5)
        avg_data.append(temp_data)

        if len(avg_data) == halfwindow * 2:
            dt = query_dhdt[i][0]
            dp = mean(avg_data)
            r_dp = (dt, dp)
            return_data.append(r_dp)
            avg_data.pop(0)
    return return_data


def create_hourly_bins(processed_query):
    returnlist = []
    t = []
    for i in range(0, len(processed_query) - 1):
        dat = posix2utc(processed_query[i][0], '%H h ')
        h0 = posix2utc(processed_query[i][0], '%H')
        h1 = posix2utc(processed_query[i + 1][0], '%H')
        dt = processed_query[i][1]

        if h0 == h1:
            t.append(dt)

        if h0 < h1:
            new_dt = round((max(t) - min(t)), 5)
            dp = [dat, new_dt]
            print(dp)
            returnlist.append(dp)
            t = []

        if h0 == h1 and i+1 == len(processed_query) - 1:
            new_dt = round((max(t) - min(t)), 5)
            dp = [dat, new_dt]
            print(dp)
            returnlist.append(dp)
            t = []

    return returnlist


def medianfilter(querydata):
    returndata = []
    for i in range(2, len(querydata)-2):
        d0 = round(float(querydata[i - 2][1]), 5)
        d1 = round(float(querydata[i - 1][1]), 5)
        d2 = round(float(querydata[i][1]), 5)
        d3 = round(float(querydata[i + 1][1]), 5)
        d4 = round(float(querydata[i + 2][1]), 5)
        d = median([d0, d1, d2, d3, d4])
        dt = querydata[i][0]
        returndata.append((dt, d))
    return returndata


def get_sigma(processed_query):
    t = []
    for item in processed_query:
        t.append(item[1])
    s = round(stdev(t), 5)
    return s


def load_sigma_list():
    returnlist = []
    if os.path.exists(sigma_file) is True:
        try:
            returnlist = pickle.load(open(sigma_file, "rb"))
        except EOFError:
            print("Pickle file is empty")
    print("Pickle file is " + str(len(returnlist)) + " records long")
    return returnlist


def append_sigma(sigmavalue, list_of_sigmas):
    list_of_sigmas.append(sigmavalue)


def check_prune_sigmas(list_of_sigmas, medianvalue):
    # db is tapped every 5 mins =  288 times
    returnlist = []
    maxlen = 288 * 27 * 3
    if len(list_of_sigmas) > maxlen:
        returnlist.append(medianvalue)
    else:
        returnlist = list_of_sigmas
    return  returnlist


def save_sigma_list(list_of_sigmas, sigma_file):
    pickle.dump(list_of_sigmas, open(sigma_file, "wb"),0)


def get_median_sigma(list_of_sigmas):
    return median(list_of_sigmas)


def colours_stdev(processed_query, median_sigma):
    # Unique to each station. Empirically derived
    scaling_factor = 2.5
    colours = []
    low1 = "#00e13c"
    low2 = "#00691c"
    med1 = "#ebb000"
    med2 = "#e14400"
    hi = "#c30012"
    for item in processed_query:
        value = item[1]
        if value < median_sigma * scaling_factor:
            clr = low1
        if value >= median_sigma * 1 * scaling_factor:
            clr = low2
        if value >= median_sigma * 2 * scaling_factor:
            clr = med1
        if value >= median_sigma * 3 * scaling_factor:
            clr = med2
        if value >= median_sigma * 4 * scaling_factor:
            clr = hi
        colours.append(clr)
    return colours


if __name__ == "__main__":
    querydata = get_data(station)
    data = []
    hours = []
    colourlist = []

    processed_query = medianfilter(querydata)
    processed_query = dxdt(processed_query)
    processed_query = average_out(processed_query)
    processed_query = create_hourly_bins(processed_query)
    if len(processed_query) > 2:
        # Calculate the stdev of the data, then determine the median sigma value to use
        sigmavalue = get_sigma(processed_query)

        list_of_sigmas = load_sigma_list()
        append_sigma(sigmavalue, list_of_sigmas)
        # This is the median value of sigma over the last three carrington rotations.
        median_sigma = get_median_sigma(list_of_sigmas)
        print("Median Sigma: " + str(median_sigma))
        list_of_sigmas = check_prune_sigmas(list_of_sigmas, median_sigma)
        save_sigma_list(list_of_sigmas, sigma_file)

        # We will use the standard deviation to determin the colour of the bars in the graph
        # and generate a list of colours to be passed to the plotter
        colourlist = colours_stdev(processed_query, median_sigma)

        # # Create an alert if hourly values go over 3-sigma
        # create_alert(processed_query)

        for item in processed_query:
            hr = item[0] + " "
            dt = float(item[1])
            hours.append(hr)
            data.append(dt)

        hours.pop(len(hours)-1)
        hours.append("Now ")

        plot(hours, data, colourlist)
    else:
        print("Not enough data to process just yet.")

    print("Plot completed")
