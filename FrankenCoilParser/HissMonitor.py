"""
Generic parser for Spectrum Lab save files.
Customised for Wideband Magnetic Riometer

Data file lines have the format of:
UTCdatetime, data_a, data_b, data_c, etc...
"""
import os.path
import time
import plotly.graph_objects as go
from statistics import median, mean
from datetime import datetime
from calendar import timegm
import numpy as np
import sqlite3
import re
from statistics import stdev

# datafile = "c://temp//hiss.csv"
datafile = "hiss.csv"

regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
stationname = "dna_hiss"
# stationname = "dna_power_harmonics"
graphing_file = stationname + "_graph.csv"
median_window = 1  # Full window = halfwindow * 2 + 1
average_window = 10
database = "hiss.db"

# Each entry is Frequency, threshold_hi, threshold_lo
frequency_range = [
    [125, 60, 20],
    [240,  60, 20],
    [410,  60, 20],
    [760,  60, 5],
    [1800, 60, 5],
    [4300, 20, -20],
    [9000, 20, -20]]


def get_index(start, stop, current, length):
    i = (current - start) / (stop - start)
    i = int(i * length)
    return i


def db_create():
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    cursor.execute("drop table if exists freq")
    cursor.execute("drop table if exists measurement")

    cursor.execute("create table freq (frequency text primary key);")
    cursor.execute("create table measurement ("
                   "posixtime integer,"
                   "frequency text,"
                   "data real,"
                   "foreign key (frequency) references freq (frequency)"
                   ");")
    # Populate with initial values
    for item in frequency_range:
        cursor.execute("Insert into freq (frequency) values (?);", [item[0]])

    datab.commit()
    datab.close()


def db_addnewdata(posixdate,frequency, data):
    # YYYY-MM-DD hh:mm:ss,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz
    # 2021-11-30 23:04:38,46.139,24.359,34.259,19.015,18.768,9.669,-3.733
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    cursor.execute("insert into measurement (posixtime, frequency, data) "
                   "values (?, ?, ?);", [posixdate,frequency, data])
    print("Added data", posixdate,frequency, data)
    datab.commit()
    datab.close()


def posix_to_utc(posixtime, format):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(format)
    return utctime

def utc_to_posix(utc_time):
    date_obj = datetime.strptime(utc_time, dt_format)
    posixtime = timegm(date_obj.timetuple())
    return posixtime


def open_file(datafile):
    returnlist = []
    with open(datafile, "r") as c:
        for line in c:
            line = line.strip("\n")
            line = line.split(",")
            datething = line[0]
            if re.match(regex, datething):
                returnlist.append(line)
    return returnlist


def parse_file(list, starttime):
    starttime = starttime
    returnlist = []
    for line in list:
        # line = line.strip("\n")
        # line = line.split(",")
        datething = line[0]
        if re.match(regex, datething):
            if utc_to_posix(datething) > starttime:
                returnlist.append(line)
    return returnlist


def db_getdatetime():
    returnvalue = 0
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    queryresult = cursor.execute("select max(posixtime) from measurement;")
    for item in queryresult:
        if item[0] is not None:
            returnvalue = item[0]
    return returnvalue


def db_get_plotdata(frequency):
    returnvalue = []
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    queryresult = cursor.execute("select * from measurement where frequency = ? order by posixtime asc;", [frequency])
    for item in queryresult:
        dp = [str(item[0]), item[2]]
        returnvalue.append(dp)
    return returnvalue


def db_get_dates(frequency):
    returnvalue = []
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    queryresult = cursor.execute("select posixtime from measurement where frequency = ? order by posixtime asc;", [frequency])
    for item in queryresult:
        dp = [str(item[0])]
        returnvalue.append(dp)
    return returnvalue


def process_dates(dates):
    returnarray = []
    for item in dates:
        plot_date = str(posix_to_utc(item[0], "%Y-%m-%d"))
        if plot_date not in returnarray:
            returnarray.append(plot_date)
    return returnarray


def db_gettimeslots():
    returnarray = []
    for i in range(0, 86400):
        if i % 300 == 0:
            returnarray.append(posix_to_utc(i, "%H:%M"))
    return returnarray


def process_data(rawplotdata, thresh_hi, thresh_lo):
    threshold_hi = thresh_hi
    threshold_lo = thresh_lo
    diff_threshold = 20
    plotnull = None
    returnarray = []
    day = []

    for i in range(1, len(rawplotdata)):
        now_time = rawplotdata[i][0]
        now_data = rawplotdata[i][1]
        prev_data = rawplotdata[i - 1][1]

        if prev_data > now_data:
            diff = prev_data - now_data
        if now_data > prev_data:
            diff = now_data - prev_data
        if now_data == prev_data:
            diff = 0

        # if now_data == 0.0:
        #     now_data = plotnull
        if now_data > threshold_hi:
            now_data = plotnull
        elif now_data < threshold_lo:
            now_data = plotnull
        elif diff > diff_threshold:
            now_data = plotnull

        day.append(now_data)

        if posix_to_utc(now_time, "%H:%M") == "00:00":
            returnarray.append(day)
            day = []
    returnarray.append(day)
    return returnarray


def plot_heatmap(slots, dates, plotdata, savefile, frequency, rows):
    data = go.Heatmap(x=slots, y=dates, z=plotdata, colorscale='hot')
    fig = go.Figure(data)
    plottitle = "VLF hiss at " + str(frequency) + " Hz. Strength in dB."
    if rows < 10:
        height = 300
    else:
        height = int(rows) * 30
    fig.update_layout(paper_bgcolor="#a0a0a0",  plot_bgcolor="#e0e0e0")
    fig.update_yaxes(tickformat="%b %d", ticklabelmode="instant")
    fig.update_layout(title_font_size=21, yaxis = dict(tickfont=dict(size=12)))
    fig.update_layout(width=1200, height=height, title=plottitle)
    # # fig.show()
    fig.write_image(savefile)


def generate_plots():
    # Create the heat plots for each frequency
    dates = db_get_dates(125)
    dates = process_dates(dates)
    slots = db_gettimeslots()
    rows = len(dates)

    for item in frequency_range:
        frequency = item[0]
        thresh_hi = item[1]
        thresh_lo = item[2]

        plotdata = db_get_plotdata(frequency)
        plotdata = process_data(plotdata, thresh_hi, thresh_lo)

        savefile = str(frequency) + ".svg"
        plot_heatmap(slots, dates, plotdata, savefile, frequency, rows)
    print("SVG iles update")


if __name__ == "__main__":
    if os.path.isfile(database) is False:
        print("No database - creating.")
        db_create()

    # Open the hiss CSV file. Load into a list
    datalist = open_file(datafile)
    #  get rid of any potential header
    datalist.pop(0)
    print("Load hiss file...")

    # Query database for most recent datetime
    print("Looking in Database for most recent start date...")
    start_posix = db_getdatetime()

    # If database is empty, get start time from CSV file
    if start_posix == 0:
        print("Database empty! Calculating start date from CSV data...")
        start_posix = utc_to_posix(datalist[0][0])
    print("Start date located: ", posix_to_utc(start_posix, dt_format))

    # The end date for calculations from CSV file
    end_posix = utc_to_posix(datalist[len(datalist) - 1][0])
    print("End date located: ", posix_to_utc(end_posix, dt_format))

    if start_posix >= end_posix:
        print("Start Date is later than End date. Stopping")
        generate_plots()
    else:
        # Create the master list of bins to populate with data from the hiss file.
        masterlist =[]
        bin_size = 60 * 5

        for i in range(start_posix, end_posix + bin_size):
            if i % bin_size == 0:
                temp_bins = []
                temp_bins.append(i)
                for j in range(1, 8):
                    temp_bins.append([0.0])
                masterlist.append(temp_bins)

        # Append data to the master list.
        print("Begin assembling array of new data values...")
        for item in datalist:
            posix_date = utc_to_posix(item[0])

            if posix_date > start_posix:
                master_range = len(masterlist) - 1
                master_index = get_index(start_posix, end_posix, posix_date, master_range)

                for i in range(1, len(item)):
                    # print(i, item, master_index, master_range)
                    data = float(item[i])
                    masterlist[master_index][i].append(data)

        datab = sqlite3.connect(database)
        cursor = datab.cursor()
        for item in masterlist:
            posixdate = item[0]

            for i in range(1, len(frequency_range) + 1):
                index = i - 1
                data = round(mean(item[i]), 3)
                cursor.execute("insert into measurement (posixtime, frequency, data) "
                               "values (?, ?, ?);", [posixdate, frequency_range[index][0], data])
                # print("Added data", posixdate, frequency_range[index], data)
        datab.commit()
        datab.close()

        generate_plots()

