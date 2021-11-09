"""
This file just trims down larger log files.
"""
import re
import time
import calendar
import datetime

datafile = "hiss.csv"
# datafile = "c://temp//hiss.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
stationname = "dna_hiss"
graphing_file = stationname + "_graph.csv"
begin_time = time.time() - (86400 * 1)


def recursive_smooth(x_now, smoothed_prev):
    # Exponential smoothing
    k = 0.5
    return (k * x_now) + ((1 - k) * smoothed_prev)


def utc_to_posix(utc_time):
    date_obj = datetime.datetime.strptime(utc_time, dt_format)
    posixtime = calendar.timegm(date_obj.timetuple())
    return posixtime


if __name__ == "__main__":
    # open master csv data, load into array
    initial_datalist = []
    refined_datalist = []

    # ***********************************************************************************
    # for master lists with several columns, parse out the data column, ignore the others
    # ***********************************************************************************
    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line_s = line.split(",")
            datething = line_s[0]

            if re.match(regex, datething):
                dt = utc_to_posix(datething)
                if dt > begin_time:
                    initial_datalist.append(line)

    # create the display file for upload to DunedinAurora.NZ
    #  Smooth the data
    with open(graphing_file, "w") as g:
        g.write("UTC Datetime,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz \n")
        for i in range(1, len(initial_datalist)):
            data = initial_datalist[i].split(",")
            data_string = data[0] + ","
            for j in range(1, len(data)):

    g.close()
    print("Data files created")

