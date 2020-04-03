"""
This file just trims down larger log files.
"""
import re
import time
import calendar
import datetime


datafile = "power_harmonics.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
stationname = "dna_power_harmonics"
graphing_file = stationname + "_graph.csv"
begin_time = time.time() - (86400 * 1)


def utc_to_posix(utc_time):
    date_obj = datetime.datetime.strptime(utc_time, dt_format)
    posixtime = calendar.timegm(date_obj.timetuple())
    return posixtime


if __name__ == "__main__":
    # open master csv data, load into array
    datalist = []

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
                    datalist.append(line)

    # create the display file for upload to DunedinAurora.NZ
    with open(graphing_file, "w") as g:
        for line in datalist:
            g.write(str(line))
    g.close()
    print("Data files created")

