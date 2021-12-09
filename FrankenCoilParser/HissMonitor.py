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


class Bin:
    def __init__(self, posixtime):
        self.posixtime = posixtime
        self.d125 = [0]
        self.d240 = [0]
        self.d410 = [0]
        self.d760 = [0]
        self.d1800 = [0]
        self.d4300 = [0]
        self.d9000 = [0]


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


def get_index(current_value, start_value, binsize):
    index = int((current_value - start_value) / binsize)
    return index


if __name__ == "__main__":
    if os.path.isfile(database) is False:
        print("No database - creating.")
        db_create()

    # Query database for most recent datetime
    now_posix = int(time.time())
    recent_posix = db_getdatetime()
    if recent_posix == 0:
        recent_posix = now_posix - (86400 * 2)

    print("Get most recent date of data insertion from database...")

    # Open the hiss CSV file. Load into a list
    datalist = open_file(datafile)
    print("Load hiss file...")

    # Most recent data to add to DB
    data_recent = parse_file(datalist, recent_posix)
    print("Parse out new data to add...")

    # Create the bin array
    binlist = []
    binsize = 60 * 5
    for i in range(recent_posix, now_posix, binsize):
        binlist.append(Bin(i))

    for item in data_recent:
        current_date = utc_to_posix(item[0])
        index = get_index(current_date, recent_posix, binsize)
        binlist[index].d125.append(float(item[1]))
        binlist[index].d240.append(float(item[2]))
        binlist[index].d410.append(float(item[3]))
        binlist[index].d760.append(float(item[4]))
        binlist[index].d1800.append(float(item[5]))
        binlist[index].d4300.append(float(item[6]))
        binlist[index].d9000.append(float(item[7]))

    # iNPUT THE BINNED DATA INTO THE DATABASE
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    for item in binlist:
        posixtime = item.posixtime
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime, 125, round(mean(item.d125), 3)])
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime,240, round(mean(item.d240), 3)])
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime, 410, round(mean(item.d410), 3)])
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime, 760, round(mean(item.d760), 3)])
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime, 1800, round(mean(item.d1800), 3)])
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime, 4300, round(mean(item.d4300), 3)])
        cursor.execute("insert into measurement (posixtime, frequency, data) "
                       "values (?, ?, ?);", [posixtime, 9000, round(mean(item.d9000), 3)])

    datab.commit()
    datab.close()



