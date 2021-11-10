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
    x_n = float(x_now)
    x_p = float(smoothed_prev)
    x_new = (k * x_n) + ((1 - k) * x_p)
    return x_new


def utc_to_posix(utc_time):
    date_obj = datetime.datetime.strptime(utc_time, dt_format)
    posixtime = calendar.timegm(date_obj.timetuple())
    return posixtime


if __name__ == "__main__":
    # open master csv data, load into array
    raw_datalist = []
    refined_datalist = []

    # ***********************************************************************************
    # for master lists with several columns, parse out the data column, ignore the others
    # ***********************************************************************************
    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line_s = line.split(",")
            datething = line_s[0]
            #  Get only the last 24 hours of data
            if re.match(regex, datething):
                dt = utc_to_posix(datething)
                if dt > begin_time:
                    raw_datalist.append(line)

    initialvalue = raw_datalist[0]
    refined_datalist.append(initialvalue)

    for i in range(1, len(raw_datalist)):
        # The new row to be appended to the refined data
        dp = []
        date = raw_datalist[i][0]
        dp.append(date)
        # recursive smooth the data and build up the datapoint
        for j in range(1, len(raw_datalist[i])):
            x_now = raw_datalist[i][j]
            smoothed_prev = refined_datalist[i-1][j]
            print(x_now, smoothed_prev)
            d = recursive_smooth(x_now, smoothed_prev)
            dp.append(d)
        #append the smoothed data
        refined_datalist.append(dp)


    # create the display file for upload to DunedinAurora.NZ
    #  Smooth the data
    with open(graphing_file, "w") as g:
        g.write("UTC Datetime,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz \n")
        for i in range(1, len(refined_datalist)):
            d = refined_datalist[i] + "\n"
            g.write(d)
    g.close()
    print("Data files created")

