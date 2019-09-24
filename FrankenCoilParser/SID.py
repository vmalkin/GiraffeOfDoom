import re
import time
import calendar
import datetime


# datafile = "/home/vmalkin/.wine/drive_c/Spectrum/screenshots/SID.csv"
datafile = "SID.csv"
# outputfile = "/home/vmalkin/Magnetometer/publish/vlf_sid.csv"
outputfile = "vlf_sid.csv"

regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
datalist = []


class DataPoint:
    def __init__(self, utc_time, data1, data2):
        self.utc_time = utc_time
        self.data1 = data1
        self.data2 = data2

    def utc_to_posix(self):
        date_obj = datetime.datetime.strptime(self.utc_time, dt_format)
        posixtime = round(calendar.timegm(date_obj.timetuple()),0)
        return posixtime

    def print_header(self):
        return "DateTime UTC, NWC, HWU)"

    def print_values(self):
        returnstring = str(self.utc_time) + "," + str(self.data1) + "," + str(self.data2)
        return returnstring


if __name__ == "__main__":
    # open master csv data, load into array
    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line = line.split(",")
            if len(line) == 4:
                dp = DataPoint(line[0], line[1], line[2].strip())
                if re.match(regex, line[0]):
                    datalist.append(dp)

    # parse out the data for the current 24 hours
    returnlist = []
    endtime = round(time.time(),0)
    starttime = int(endtime - 86400)

    for dp in datalist:
        print(str(dp.utc_to_posix()) + " " + str(starttime))
        if dp.utc_to_posix() > starttime:
            returnlist.append(dp)

    # create the display file for upload to DunedinAurora.NZ
    with open(outputfile, "w") as g:
        g.write(returnlist[0].print_header() + "\n")

        for dp in returnlist:
            g.write(dp.print_values() + "\n")
    g.close()
