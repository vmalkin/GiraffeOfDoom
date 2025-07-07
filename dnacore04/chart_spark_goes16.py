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

# #######################################################################################
#   These details must be cusomised for each station
sigma_file = "s_goes.pkl"
mean_file = "m_goes.pkl"
station = "GOES_16"
plot_title = "Magnetometer dh/dt<br>GOES East"
median_sigma = 0
median_mean = 0
# a 10 min window for averaging readings give the number of readings per minute
halfwindow = 10
# Empirically derived scaling factor to make date fit the appropriate colour range
scaling_factor = 1
# #######################################################################################

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

# hours, data, colourlist, min_value, median_sigma
def plot(hours, data, colours):
    maxaxis = 8 * median_sigma + median_mean
    fig = go.Figure(go.Bar(
        x=data,
        y=hours,
        marker=dict(color=colours),
        orientation='h'
    ))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(width=300, height=1200, title=plot_title,
                      xaxis=dict(tickmode="array",
                                 tickvals=[median_mean,
                                           median_mean + 2 * median_sigma,
                                           median_mean + 4 * median_sigma,
                                           median_mean + 6 * median_sigma,
                                           median_mean + 8 * median_sigma],
                                 ticktext=["x", "2σ", "4σ", "6σ", "8σ"]))

    fig.update_layout(font=dict(size=20, color='#ffffff'), margin=dict(l=10, r=20, b=10), yaxis_title="UTC")
    fig.update_xaxes(range=[0, maxaxis], gridcolor='#505050', visible=True)
    savefile = "spk_" + station + ".svg"
    # savefile = "spk_test.svg"
    fig.write_image(file=savefile, format='svg')


def dxdt(querydata):
    # calculate the rate of change, dx/dt
    t = []
    for i in range(1, len(querydata)):
        dt = querydata[i][0]
        d2 = float(querydata[i][1])
        d1 = float(querydata[i-1][1])

        dh = round((d2 - d1), 7)
        dp = (dt, dh)

        t.append(dp)
    return t


def average_out(query_dhdt):
    # smoothes out the dh/dt data
    avg_data = []
    return_data = []

    for i in range(0, len(query_dhdt)):
        temp_data = float(query_dhdt[i][1])
        temp_data = round(temp_data, 7)
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
    processed_query.reverse()
    # we will be iterating backwards
    h0 = processed_query[0][0]
    for i in range(1, len(processed_query) - 1):
        h1 = processed_query[i][0]
        d = processed_query[i][1]
        if (h0 - h1) < (60*60):
            t.append(d)
        else:
            dat = posix2utc(h0, "%H:%M")
            d = max(t) - min(t)
            dp = [dat, d]
            returnlist.append(dp)
            h0 = h1
            t = []
    returnlist.reverse()
    return returnlist


def medianfilter(querydata):
    returndata = []
    for i in range(2, len(querydata)-2):
        d0 = round(float(querydata[i - 2][1]), 7)
        d1 = round(float(querydata[i - 1][1]), 7)
        d2 = round(float(querydata[i][1]), 7)
        d3 = round(float(querydata[i + 1][1]), 7)
        d4 = round(float(querydata[i + 2][1]), 7)
        d = median([d0, d1, d2, d3, d4])
        dt = querydata[i][0]
        returndata.append((dt, d))
    return returndata


def get_sigma(processed_query):
    t = []
    for item in processed_query:
        t.append(item[1])
    s = round(stdev(t), 7)
    return s

def get_mean(processed_query):
    t = []
    for item in processed_query:
        t.append(item[1])
    s = round(mean(t), 7)
    return s


def load_data_list(filename):
    returnlist = []
    if os.path.exists(filename) is True:
        try:
            returnlist = pickle.load(open(filename, "rb"))
        except EOFError:
            print("Pickle file is empty")
    print("Pickle file is " + str(len(returnlist)) + " records long")
    return returnlist


def append_value(value, list_of_values):
    list_of_values.append(value)


def check_prune_value(list_of_values, value):
    # db is tapped every 5 mins =  288 times
    returnlist = []
    maxlen = 288 * 27 * 3
    if len(list_of_values) > maxlen:
        returnlist.append(value)
    else:
        returnlist = list_of_values
    return  returnlist


def save_data_list(list_of_values, values_file):
    pickle.dump(list_of_values, open(values_file, "wb"),0)


def get_median_value(list_of_values):
    return median(list_of_values)


def colours_stdev(processed_query, mean, mediansigma):
    # Unique to each station. Empirically derived
    colours = []
    clr = "#ffffff"
    low1 = "#00c31a"  # med green
    low2 = "#00790f"  # dark green
    med1 = "#e17100"  # orange
    hi1 = "#900000"  # red

    for item in processed_query:
        value = item[1]
        if value > 0:
            clr = low1
        if value > mean + (mediansigma * 1 * scaling_factor):
            clr = low1
        if value > mean + (mediansigma * 2 * scaling_factor):
            clr = low2
        if value > mean + (mediansigma * 3 * scaling_factor):
            clr = med1
        if value > mean + (mediansigma * 5 * scaling_factor):
            clr = med1
        if value > mean + (mediansigma * 7 * scaling_factor):
            clr = hi1

        colours.append(clr)
    return colours


# def get_min_value(processed_query):
#     t = []
#     for item in processed_query:
#         t.append(item[1])
#     return min(t)


def hours_to_stdevs(processed_query):
    returnresult = []
    for item in processed_query:
        dt = item[0]
        da = item[1]


def create_alert(alerttext):
    db = dna_core.cursor()
    t = int(time())
    values = [station, t, alerttext]
    try:
        db.execute("insert into events (station_id, posix_time, message) values (?,?,?)", values)
        dna_core.commit()
    except sqlite3.Error:
        print("DATABASE ERROR inserting new alert")
    db.close()


def processalerts(processed_query, median_mean, median_sigma):
    returnvalue = ""
    k = len(processed_query)-1
    nowdata = processed_query[k][1]

    if nowdata <= median_mean + (median_sigma * 4 * scaling_factor):
        returnvalue = plot_title + ": Geomagnetic activity has been quiet in the last 60 mins."
    if nowdata > median_mean + (median_sigma * 4 * scaling_factor):
        returnvalue = plot_title + ": Geomagnetic activity has been unsettled in the last 60 mins."
    if nowdata > median_mean + (median_sigma * 6 * scaling_factor):
        returnvalue = plot_title + ": Geomagnetic activity has been moderate in the last 60 mins."
    if nowdata > median_mean + (median_sigma * 7 * scaling_factor):
        returnvalue = plot_title + ": Geomagnetic activity has been STRONG in the last 60 mins."

    for item in processed_query:
        dt = item[0]
        dt = dt.split(":")
        dt = dt[0]+"hrs"
        value = item[1]
        r=""
        if value >= median_mean + (median_sigma * 4 * scaling_factor):
            r = "\n" + dt + " UTC: " + "Unsettled activity detected."
        if value > median_mean + (median_sigma * 6 * scaling_factor):
            r = "\n" + dt + " UTC: " + "moderate activity detected."
        if value > median_mean + (median_sigma * 7 * scaling_factor):
            r = "\n" + dt + " UTC: " + "STRONG activity detected."
        returnvalue = returnvalue + r

    return returnvalue


def process_dashboard(processed_query, median_mean, median_sigma):
    returnvalue = ""
    k = len(processed_query)-1
    nowdata = processed_query[k][1]

    if nowdata <= median_mean + (median_sigma * 3 * scaling_factor):
        returnvalue = "none"
    if nowdata > median_mean + (median_sigma * 4 * scaling_factor):
        returnvalue = "low"
    if nowdata > median_mean + (median_sigma * 6 * scaling_factor):
        returnvalue = "med"
    if nowdata > median_mean + (median_sigma * 7 * scaling_factor):
        returnvalue = "high"
    return returnvalue


def create_dashboard(dash_msg):
    db = dna_core.cursor()
    t = int(time())
    values = [station, t, dash_msg]
    try:
        db.execute("insert into dashboard (station_id, posix_time, message) values (?,?,?)", values)
        dna_core.commit()
    except sqlite3.Error:
        print("DATABASE ERROR inserting new alert")
    db.close()


if __name__ == "__main__":
    querydata = get_data(station)
    data = []
    hours = []
    colourlist = []

    processed_query = medianfilter(querydata)
    processed_query = dxdt(processed_query)
    processed_query = average_out(processed_query)
    processed_query = create_hourly_bins(processed_query)
    print(len(processed_query))

    if len(processed_query) > 2:
        # Calculate the stdev of the data, then determine the median sigma value to use
        sigmavalue = get_sigma(processed_query)
        meanvalue = get_mean(processed_query)

        list_of_sigmas = load_data_list(sigma_file)
        list_of_means = load_data_list(mean_file)

        append_value(sigmavalue, list_of_sigmas)
        append_value(meanvalue, list_of_means)
        # This is the median value of sigma over the last three carrington rotations.
        median_sigma = get_median_value(list_of_sigmas)
        median_mean = get_median_value(list_of_means)

        print("Median Sigma: " + str(median_sigma))
        print("Median Mean: " + str(median_mean))

        list_of_sigmas = check_prune_value(list_of_sigmas, median_sigma)
        list_of_means = check_prune_value(list_of_sigmas, median_sigma)

        save_data_list(list_of_sigmas, sigma_file)
        save_data_list(list_of_means, mean_file)

        # Convert actual values to standard deviations
        stdevhours = hours_to_stdevs(processed_query)

        # colours are determined by the median standard deviation.
        colourlist = colours_stdev(processed_query, median_mean, median_sigma)

        for item in processed_query:
            hr = item[0] + " "
            dt = float(item[1])
            hours.append(hr)
            data.append(dt)

        hours.pop(len(hours)-1)
        hours.append("Now ")

        # Create an alert if hourly values go over 3-sigma
        alertmessage = processalerts(processed_query, median_mean, median_sigma)
        if len(alertmessage) > 0:
            print(alertmessage)
            if len(list_of_sigmas) < 400:
                alertmessage = alertmessage + "\nComputer is refining threshold values"
            create_alert(alertmessage)

        # Create data for the DnA dashboard
        dashb_msg = process_dashboard(processed_query, median_mean, median_sigma)
        if len(dashb_msg) > 0:
            print(dashb_msg)
            create_dashboard(dashb_msg)

        plot(hours, data, colourlist)
    else:
        print("Not enough data to process just yet.")

    print("Plot completed")
