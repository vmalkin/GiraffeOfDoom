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
        self.data = [0]

    def avg_data(self):
        return mean(self.data)

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


def db_addnewdata(data_recent):
    # YYYY-MM-DD hh:mm:ss,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz
    # 2021-11-30 23:04:38,46.139,24.359,34.259,19.015,18.768,9.669,-3.733
    datab = sqlite3.connect(database)
    cursor = datab.cursor()

    for item in data_recent:
        measurement_date = utc_to_posix(item[0])
        item.pop(0)

        for i in range(0, len(frequency_range)):
            posixtime = measurement_date
            cursor.execute("insert into measurement (posixtime, frequency, data) "
                           "values (?, ?, ?);", [measurement_date,frequency_range[i], item[i]])
            print("Added data", posix_to_utc(measurement_date),frequency_range[i], item[i])
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
    datab = sqlite3.connect(database)
    cursor = datab.cursor()
    queryresult = cursor.execute("select max(posixtime) from measurement;")
    for item in queryresult:
        if item[0] == None:
            returnvalue = 0
        else:
            returnvalue = item[0]
    return returnvalue


if __name__ == "__main__":
    if os.path.isfile(database) is False:
        print("No database - creating.")
        db_create()

    # Query database for most recent datetime
    recent_posix = db_getdatetime()
    print("Get most recent date of data insertion from database")

    # Open the hiss CSV file. Load into a list
    datalist = open_file(datafile)
    print("Load hiss file")

    # Most recent data to add to DB
    data_recent = parse_file(datalist, recent_posix)
    print("Parse out new data to add")

    #  Convert the data into a numpy list, get the number of elements in each row.
    npdata = np.array(data_recent)
    rowlen = npdata.shape[1]

    # Slice the array into separate lists for each column
    master_data = []
    datetimes = npdata[:, 0]
    for i in range(1, rowlen):
        master_data.append(npdata[:, i])


    # Generate the binlist
    print("Generating bin lists for processing")
    master_binlists = []
    binlist = []
    binsize = 60 * 5
    for i in range(recent_posix, time.time(), binsize):
        binlist.append(Bin(i))





