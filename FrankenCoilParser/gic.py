import re
import time
import calendar
import datetime

datafile = "gic.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M"
datalist = []

class DataPoint:
    def __init__(self, utc_time, datapoint):
        self.utc_time = utc_time
        self.datapoint = datapoint

    def utc_to_posix(self):
        date_obj = datetime.datetime.strptime(self.utc_time, dt_format)
        posixtime = calendar.timegm(date_obj.timetuple())
        return posixtime

    def print_header(self):
        return "DateTime UTC, Harmonic Frequency"

    def print_values(self):
        returnstring = self.utc_time + "," + self.datapoint
        return returnstring

if __name__ == "__main__":
    # open master csv data, load into array

    with open(datafile, "r") as c:
        for line in c:
            line.strip("\n")
            line = line.split(",")
            dp = DataPoint(line[0], line[1].strip())
            if re.match(regex, line[0]):
                datalist.append(dp)

    # parse out the data for the current 24 hours
    returnlist = []
    endtime = time.time()
    starttime = endtime - 86400

    for dp in datalist:
        if dp.utc_to_posix() > starttime:
            returnlist.append(dp)

    # create the display file for upload to DunedinAurora.NZ
    with open("induction_gic.csv", "w") as g:
        g.write(returnlist[0].print_header() + "\n")

        for dp in returnlist:
            g.write(dp.print_values() + "\n")
    g.close()

