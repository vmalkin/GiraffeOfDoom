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

errorloglevel = logging.WARNING
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
sigma_file = "sigmas.pkl"


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


def plot(hours, data):
    fig = go.Figure(go.Bar(
        x=data,
        y=hours,
        orientation='h'
    ))
    fig.update_traces(marker_line_width=1, marker_line_color='#007000')
    fig.show()


def dxdt(querydata):
    # calculate the rate of change, dx/dt
    t = []
    for i in range(1, len(querydata)):
        dt = querydata[i][0]
        d2 = float(querydata[i][1])
        d1 = float(querydata[i-1][1])

        dh = round((d2 - d1),3)
        dp = (dt, dh)

        t.append(dp)
    return t


def average_out(query_dhdt):
    # smoothes out the dh/dt data
    # a 10 min window for 30 readings per min
    halfwindow = 30 * 10
    avg_data = []
    return_data = []

    for i in range(0, len(query_dhdt)):
        temp_data = float(query_dhdt[i][1])
        temp_data = round(temp_data, 3)
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
        h0 = posix2utc(processed_query[i][0], '%H')
        h1 = posix2utc(processed_query[i + 1][0], '%H')
        dt = processed_query[i][1]

        if h0 == h1:
            t.append(dt)
        else:
            new_dt = round((max(t) - min(t)),5)
            dp = [h0, new_dt]
            print(dp)
            returnlist.append(dp)
            t = []
    return returnlist


def medianfilter(querydata):
    returndata = []
    for i in range(2, len(querydata)-2):
        d0 = round(float(querydata[i - 2][1]), 3)
        d1 = round(float(querydata[i - 1][1]), 3)
        d2 = round(float(querydata[i][1]), 3)
        d3 = round(float(querydata[i + 1][1]), 3)
        d4 = round(float(querydata[i + 2][1]), 3)
        d = median([d0, d1, d2, d3, d4])
        dt = querydata[i][0]
        returndata.append((dt, d))
    return returndata


def get_sigma(processed_query):
    t = []
    for item in processed_query:
        t.append(item[1])
    s = stdev(t)
    return s





if __name__ == "__main__":
    querydata = get_data("Ruru_Obs")
    data = []
    hours = []

    # If there is enough data to process
    if len(querydata) > (30*30):
        processed_query = medianfilter(querydata)
        processed_query = dxdt(processed_query)
        processed_query = average_out(processed_query)
        processed_query = create_hourly_bins(processed_query)

        # Calculate the stdev of the data, then determine the median sigma value to use
        sigmavalue = get_sigma(processed_query)
        list_of_sigmas = load_sigma_list(sigma_file)
        append_sigma(sigmavalue)
        list_of_sigmas = check_prune_sigmas(list_of_sigmas, sigma_file)
        save_sigma_list(list_of_sigmas, sigma_file)
        median_sigma = get_median_sigma(list_of_sigmas)

        # We will use the standard deviation to determin the colour of the bars in the graph
        # and generate a list of colours to be passed to the plotter
        colourlist = colours_stdev(processed_query, median_sigma)

        # Create an alert if hourly values go over 3-sigma
        create_alert(processed_query)

        for item in processed_query:
            hr = item[0] + " hrs"
            dt = float(item[1])
            hours.append(hr)
            data.append(dt)

        plot(hours, data, colourlist)
    else:
        print("Not enough data to process just yet.")

