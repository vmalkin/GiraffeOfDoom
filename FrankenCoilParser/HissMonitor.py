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
frequency_range = [125, 240, 410, 760, 1800, 4300, 9000]


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
        cursor.execute("Insert into freq (frequency) values (?);", [item])

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


# def filter_average(list):
#     returnlist = []
#     for i in range(average_window, len(list) - average_window):
#         templist = []
#         for j in range(-1 * average_window, average_window):
#             data = float(list[i+j])
#             templist.append(data)
#         avg_data = mean(templist)
#         avg_data = round(avg_data, 3)
#         returnlist.append(avg_data)
#     return returnlist


# def filter_median(item_list):
#     """
#     Takes in a list of DataPoints and performs a median filter on the list. The list is truncated at the start
#     and end by one halfwindow
#     """
#     returnlist = []
#
#     for i in range(median_window, len(item_list) - median_window):
#         data_store = []
#         for j in range(0 - median_window, median_window + 1):
#             d = float(item_list[i + j])
#             data_store.append(d)
#         medianvalue = median(data_store)
#         returnlist.append(medianvalue)
#     return returnlist


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

#
# def get_header(datafile):
#     with open(datafile, "r") as c:
#         for line in c:
#             line = line.strip()
#             header = line
#             break
#     return header

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


# def filter_nulls(data):
#     null = None
#     returnlist = []
#     for item in data:
#         if item == 0:
#             returnlist.append(null)
#         elif item > 500:
#             returnlist.append(null)
#         else:
#             returnlist.append(item)
#     return returnlist


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


def process_data(plotdata):
    returnarray = []
    day = []
    for item in plotdata:
        plot_date = item[0]
        plot_data = item[1]
        day.append(plot_data)
        if posix_to_utc(plot_date, "%H:%M") == "00:00":
            returnarray.append(day)
            day = []
    return returnarray


def plot_heatmap(slots, dates, plotdata, savefile, frequency, rows):
    data = go.Heatmap(x=slots, y=dates, z=plotdata, colorscale='thermal')
    fig = go.Figure(data)
    plottitle = str(frequency) + " Hz"
    height = int(rows) * 30
    fig.update_layout(width=1200, height=height, title=plottitle)
    # fig.show()
    fig.write_image(savefile)

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

    if start_posix == 0:
        print("Database empty! Calculating start date from CSV data...")
        start_posix = utc_to_posix(datalist[0][0])
    print("Start date located: ", posix_to_utc(start_posix, dt_format))
    # The end date for calculations
    end_posix = utc_to_posix(datalist[len(datalist) - 1][0])
    print("End date located: ", posix_to_utc(end_posix, dt_format))

    if start_posix >= end_posix:
        print("Start Date is later than End date. Stopping")
    else:
        # Create the master list of bins to populate with data from the hiss file.
        masterlist =[]
        bin_size = 60 * 5

        for i in range(start_posix, end_posix + bin_size):
            if i % bin_size == 0:
                temp_bins = []
                temp_bins.append(i)
                for j in range(1, 8):
                    temp_bins.append([])
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
                               "values (?, ?, ?);", [posixdate, frequency_range[index], data])
                print("Added data", posixdate, frequency_range[index], data)
        datab.commit()
        datab.close()


    dates = db_get_dates(125)
    dates = process_dates(dates)
    slots = db_gettimeslots()
    rows = len(dates)

    for freq in frequency_range:
        plotdata = db_get_plotdata(freq)
        plotdata = process_data(plotdata)
        savefile = str(freq) + ".jpg"
        plot_heatmap(slots, dates, plotdata, savefile, freq, rows)

