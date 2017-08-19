import DataPoint
import math
import os
from decimal import Decimal

__author__ = "Meepo"

# #######################
# constructor
# #######################
class Station:
    def __init__(self, station_name, csvfile):
        self.csvfile = csvfile
        self.station_name = station_name
        self.datapointarray = []
        self.output_f = []

        # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
        if os.path.isfile(csvfile):

            x = 0
            with open(csvfile) as r:
                for line in r:
                    x = x + 1
                    # print(csvfile + " " + str(x))
                    values = line.split(",")
                    dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
                    self.datapointarray.append(dp)
            print("Array for " + self.station_name + " created, " + str(len(self.datapointarray)) + " records long")
            # print(datapointarray[0].raw_x)
        else:
            print("Unable to create list of observations for station " + self.station_name)

        # produce an array of "H" values
        for i in range(0,len(self.datapointarray)):
            h = self.datapointarray[i].raw_x
            # h = self.datapointarray[i].raw_x
            datetime = self.datapointarray[i].dateTime
            valuestring = datetime + "," + str(h)
            # print(valuestring)
            self.output_f.append(valuestring)

        # Normalise single value datadata
        temp_array = []
        datamin = Decimal(0)

        # first find the smallest value...
        for item in self.output_f:
            item = item.split(",")
            # this is now the actual value figure...
            item = Decimal(item[1])
            if item <= datamin:
                datamin = item

        datamax = Decimal(datamin)
        # now find the largets value...
        for item in self.output_f:
            item = item.split(",")
            # this is now the actual value figure...
            item = Decimal(item[1])
            if item > datamax:
                datamax = item

        temp_array = []

        print(self.station_name + " max/min values: " + str(datamax) + "/" + str(datamin))

        diffvalue = datamax - datamin
        for i in range(0, len(self.output_f)):
            datastring = self.output_f[i].split(",")
            datavalue = (Decimal(datastring[1]) - datamin) / diffvalue
            newdatastring = datastring[0] + "," + str(datavalue)
            temp_array.append(newdatastring)

        self.output_f = temp_array