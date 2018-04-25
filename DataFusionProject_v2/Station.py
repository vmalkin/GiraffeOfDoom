from datetime import datetime
from time import mktime
import os

__author__ = "Meepo"

class DataPoint:
    def __init__(self, date, data):
        self.date = date
        self.data = data
        self.posixtime = self.utc2posix()

    def utc2posix(self):
        posixtimestamp = 0
        try:
            # dateformat = "%Y-%m-%d %H:%M:%S.%f"
            dateformat = "%Y-%m-%d %H:%M"
            newdatetime = datetime.strptime(self.date, dateformat)
            # convert to Unix time (Seconds)
            posixtimestamp = mktime(newdatetime.timetuple())
        except:
            print("Problem with entry ")
        return posixtimestamp

    def print_values(self):
        returnstring = str(self.posixtime) + "," + str(self.data)
        return returnstring

class Station:
    def __init__(self, station_name, csvfile):
        self.csvfile = csvfile
        self.station_name = station_name
        self.datalist = self.load_csv()
        self.datalist_normalised = self.normalise()

    def normalise(self):
        data_normal = []
        min = 20000
        max = -20000
        for item in self.datalist:
            if item.data != "":
                if float(item.data) < float(min):
                    min = item.data
                elif float(item.data) > float(max):
                    max = item.data
        for item in self.datalist:
            if item.data != "":
                date = item.date
                data = (float(item.data) - float(min)) / (float(max) - float(min))
                dp = DataPoint(date, data)
                data_normal.append(dp)
        return data_normal


    # ####################################################################################
    # Load datadata from file
    # ####################################################################################
    def load_csv(self):
        importarray = []
        # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
        if os.path.isfile(self.csvfile):
            with open(self.csvfile) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    values = line.split(",")
                    dp = DataPoint(values[0], values[1])
                    importarray.append(dp)
        return importarray

    def save_csv(self):
        # export array to array-save file
        try:
            # path = "/home/vmalkin/Magnetometer/publish/"
            path = ""
            with open(path + self.station_name + "nrml.csv", 'w') as w:
                for item in self.datalist_normalised:
                    w.write(item.print_values() + '\n')
        except IOError:
            print("WARNING: There was a problem saving binned CSV datadata")







