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
    [760,  30, 5],
    [1800, 30, 5],
    [4300, 20, -10],
    [9000, 20, -10]]


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


def plot_heatmap(slots, dates, plotdata, savefile, frequency, rows, z_hi, z_lo):
    data = go.Heatmap(x=slots, y=dates, z=plotdata, colorscale='hot')
    fig = go.Figure(data)
    plottitle = "VLF hiss at " + str(frequency) + " Hz. Strength in dB."
    if rows < 10:
        height = 300
    else:
        height = int(rows) * 30
    fig.data[0].update(zmin=z_lo, zmax=z_hi)
    fig.update_layout(paper_bgcolor="#a0a0a0",  plot_bgcolor="#e0e0e0")
    fig.update_xaxes(title_text="UTC Hours")
    fig.update_yaxes(title_text="UTC Date", tickformat="%b %d", ticklabelmode="instant")
    # fig.update_yaxes(ticklabelmode="instant")
    fig.update_layout(title_font_size=21, yaxis = dict(tickfont=dict(size=12)))
    fig.update_layout(width=1200, height=height, title=plottitle)
    # fig.show()
    fig.write_image(savefile)


def create_slots():
    returnlist = []
    for i in range(0, 86400, 300):
        returnlist.append(posix_to_utc(i, "%H:%M"))
    return returnlist

def draw_graphs():
    print("Updating graphs...")
    # Get data for each frequency and begin to process.
    for item in frequency_range:
        frequency = item[0]
        thresh_hi = item[1]
        thresh_lo = item[2]

        # Get unbinned data
        rawdata = db_get_plotdata(frequency)
        data_start = int(rawdata[0][0])
        data_end = int(rawdata[len(rawdata) - 1][0])

        # Set up to create 5 min bins.
        masterlist = []
        masterlist_dates = []
        bin = 60 * 5
        for i in range(data_start, data_end):
            if i % bin == 0:
                masterlist.append([0])
                masterlist_dates.append(i)

        #  Put data from the raw data into the correct 5 min bin
        for item in rawdata:
            date = int(item[0])
            data = item[1]
            listlength = len(masterlist) - 1
            index = int(((date - data_start) / (data_end - data_start)) * listlength)
            masterlist[index].append(data)

        # We now have two lists of data, dates at 5 minute intervals and bins of data at 5 min intervals.
        # These data must be rearranged so Plotly can create a heatmap from them
        plot_total = []
        plot_daily = []
        plot_dateaxis = []
        slots = create_slots()

        for i in range(0, len(masterlist_dates)):
            # If we have reached the end of the day, create a new row to be added to the plot_total
            # This becomes a new line for the day in the heatmap.
            if posix_to_utc(masterlist_dates[i], "%H:%M") == "00:00":
                plot_total.append(plot_daily)
                plot_dateaxis.append(posix_to_utc(masterlist_dates[i]-86400, "%Y-%m-%d"))
                plot_daily = []
            else:
                # Create a single value of the data for the current 5 minutes. Catch any weird data issues.
                # this is our summary for the 5 minutes
                if sum(masterlist[i]) > 0:
                    data = mean(masterlist[i])
                elif sum(masterlist[i]) == 0:
                    data = None
                plot_daily.append(data)
        # The last row is partial data for the day
        plot_total.append(plot_daily)

        savefile = str(frequency) + ".svg"
        # plot_heatmap(slots, plot_dateaxis, plot_total, savefile, frequency, len(plot_total), None, None)
        plot_heatmap(slots, plot_dateaxis, plot_total, savefile, frequency, len(plot_total), thresh_hi, thresh_lo)
    print("All graphs updated!")


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
        print("Start Date is later than End date. No data will be imported!")
        draw_graphs()
    else:
        # Append all data into the database.
        datab = sqlite3.connect(database)
        cursor = datab.cursor()

        for item in datalist:
            posixdate = utc_to_posix(item[0])
            for i in range(1, len(frequency_range) + 1):
                index = i - 1
                rawdata = item[i]
                cursor.execute("insert into measurement (posixtime, frequency, data) "
                               "values (?, ?, ?);", [posixdate, frequency_range[index][0], rawdata])
        #         # print("Added data", posixdate, frequency_range[index], data)
        datab.commit()
        datab.close()

        draw_graphs()



