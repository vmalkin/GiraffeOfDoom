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
            with open(csvfile) as r:
                for line in r:
                    values = line.split(",")
                    dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
                    self.datapointarray.append(dp)
            print("Array for " + self.station_name + " created, " + str(len(self.datapointarray)) + " records long")
            # print(datapointarray[0].raw_x)
        else:
            print("Unable to create list of observations for station " + self.station_name)

        for i in range(0,len(self.datapointarray)):
            h = math.sqrt(math.pow(Decimal(self.datapointarray[i].raw_x),2) + math.pow(Decimal(self.datapointarray[i].raw_y),2) + math.pow(Decimal(self.datapointarray[i].raw_z),2))
            datetime = self.datapointarray[i].dateTime
            valuestring = datetime + "," + str(h)
            # print(valuestring)
            self.output_f.append(valuestring)







