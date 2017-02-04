import DataPoint
import datetime
import time
import os
from decimal import Decimal

__author__ = "Meepo"

class Station:
    def __init__(self, station_name, csvfile):
        # ############################
        # Class function definitions
        # ############################

        # ####################################################################################
        # Load CSV file. Returns datapoint array
        # ####################################################################################
        def loadcsvfile(station_name, csvfile):
            datapointarray = []
            # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
            if os.path.isfile(csvfile):
                with open(csvfile) as r:
                    for line in r:
                        values = line.split(",")
                        dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
                        datapointarray.append(dp)
                print("Array for " + station_name + " created, " + str(len(datapointarray)) + " records long")
                # print(datapointarray[0].raw_x)

                return datapointarray
            else:
                print("Unable to create list of observations for station " + self.station_name)

        # ####################################################################################
        # create and return a list/array of H values.
        # ####################################################################################
        def producehvalues(datapointarray):
            # produce an array of "H" values
            output_h = []

            for i in range(0,len(datapointarray)):
                h = datapointarray[i].raw_x
                # h = self.datapointarray[i].raw_x
                datetime = datapointarray[i].dateTime
                valuestring = datetime + "," + str(h)
                # print(valuestring)
                output_h.append(valuestring)

            return output_h


        # ####################################################################################
        # Normalises and returns H values between 1 and 0
        # ####################################################################################
        def normalisehvalues(output_f):
            # Normalise single value data
            temp_array = []
            datamin = Decimal(10000)

            # first find the smallest value...
            for item in output_f:
                item = item.split(",")
                # this is now the actual value figure...
                item = Decimal(item[1])
                if item <= datamin:
                    datamin = item

            datamax = Decimal(datamin)
            # now find the largets value...
            for item in output_f:
                item = item.split(",")
                # this is now the actual value figure...
                item = Decimal(item[1])
                if item > datamax:
                    datamax = item

            temp_array = []

            print(self.station_name + " max/min values: " + str(datamax) + "/" + str(datamin))

            diffvalue = datamax - datamin
            for i in range(0, len(output_f)):
                datastring = output_f[i].split(",")
                datavalue = (Decimal(datastring[1]) - datamin) / diffvalue
                newdatastring = datastring[0] + "," + str(datavalue)
                temp_array.append(newdatastring)


            return temp_array

        # ####################################################################################
        # converts the UTC timestamp to unix time. returns converted array.
        # ####################################################################################
        def utc2unix(output_h):
            temparray = []
            for item in output_h:
                data = item.split(",")
                utcdate = data[0]
                datavalue = data[1]

                # Make a datetime object from the string
                dt = datetime.datetime.strptime(utcdate, "%Y-%m-%d %H:%M")
                unixtime = time.mktime(dt.timetuple())

                appenddata = str(unixtime) + "," + datavalue
                temparray.append(appenddata)
            return temparray

        # ####################################################################################
        # Trim array to the last 24 hours only
        # ####################################################################################
        def trim24hour(array):
            chopvalue = len(array) - 1440

            if len(array) > 1440:
                array = array[chopvalue:]

            return array

        # ####################################################################################
        # Instantiation starts here...
        # ####################################################################################
        self.csvfile = csvfile
        self.station_name = station_name

        # process in the statin datafile
        stationdata = loadcsvfile(self.station_name, self.csvfile)

        # COnvert to H values ie: we only want the first data value a datapoint may have in this instance.
        # Datapoints that have 3 values may need to be converted to a single value here
        # trim the array to the last 24 hours
        stationdata = producehvalues(stationdata)
        stationdata = trim24hour(stationdata)

        # Normalise the data between 1 and 0
        stationdata = normalisehvalues(stationdata)
        print("Datetime range for " + self.station_name + " is: " + str(stationdata[0]) + " " + str(stationdata[len(stationdata) - 1]))

        # COnvert data timestamps to Unix time. Make accessible self.
        self.stationdata = utc2unix(stationdata)

        # A station can report the begin and end times of it's data.
        begintime = self.stationdata[0]
        begintime = begintime.split(",")
        self.begintime = begintime[0]

        endtime = self.stationdata[len(stationdata) - 1]
        endtime = endtime.split(",")
        self.endtime = endtime[0]




