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
# datafile = "c://temp//harmonics.csv"
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


def filter_average(list):
    returnlist = []
    for i in range(average_window, len(list) - average_window):
        templist = []
        for j in range(-1 * average_window, average_window):
            data = float(list[i+j])
            templist.append(data)
        avg_data = mean(templist)
        avg_data = round(avg_data, 3)
        returnlist.append(avg_data)
    return returnlist


def filter_median(item_list):
    """
    Takes in a list of DataPoints and performs a median filter on the list. The list is truncated at the start
    and end by one halfwindow
    """
    returnlist = []

    for i in range(median_window, len(item_list) - median_window):
        data_store = []
        for j in range(0 - median_window, median_window + 1):
            d = float(item_list[i + j])
            data_store.append(d)
        medianvalue = median(data_store)
        returnlist.append(medianvalue)
    return returnlist


def posix_to_utc(posixtime):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(dt_format)
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


def get_header(datafile):
    with open(datafile, "r") as c:
        for line in c:
            line = line.strip()
            header = line
            break
    return header

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


def filter_nulls(data):
    null = None
    returnlist = []
    for item in data:
        if item == 0:
            returnlist.append(null)
        elif item > 500:
            returnlist.append(null)
        else:
            returnlist.append(item)
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

    # The end date for calculations
    end_posix = utc_to_posix(datalist[len(datalist) - 1][0])

    # Create the master list of bins to populate with data from the hiss file.
    masterlist =[]
    # temp_bins = [["replace me with posix date"], [], [], [], [], [], [], []]
    bin_size = 60 * 5

    for i in range(start_posix, end_posix + bin_size):
        if i % bin_size == 0:
            temp_bins = []
            temp_bins.append(i)
            for j in range(1, 8):
                temp_bins.append([])
            masterlist.append(temp_bins)

    # Append data to the master list.
    for item in datalist:
        posix_data = utc_to_posix(item[0])
        master_range = len(masterlist) - 1
        master_index = get_index(start_posix, end_posix, posix_data, master_range)

        for i in range(1, len(item)):
            data = float(item[i])
            masterlist[master_index][i].append(data)


