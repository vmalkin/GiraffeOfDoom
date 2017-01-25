import datetime
import time
import os
from decimal import Decimal
import pickle

__author__ = "Meepo"

class Station:
    def __init__(self, station_name, csvfile):

        self.station_name = station_name
        self.csvfile = csvfile

        # ####################################################################################
        # Load CSV file. Returns datapoint array
        # ####################################################################################
        def loadcsvfile(station_name, csvfile):
            datapointarray = []
            # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
            if os.path.isfile(csvfile):
                with open(csvfile) as r:
                    for line in r:
                        dp = line
                        datapointarray.append(dp)
                print("Array for " + station_name + " created, " + str(len(datapointarray)) + " records long")

            else:
                print("Unable to create list of observations for station " + self.station_name)

                datapointarray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            return  datapointarray

        # ####################################################################################
        # Calculate diffs - dH/dt
        # ####################################################################################
        def calc_dHdt(h_values):
            returnarray = []

            for i in range(1, len(h_values)):
                # get previous values
                prev_split = h_values[i - 1].split(",")
                h_prev = prev_split[1]

                # get current values and date
                current_split = h_values[i].split(",")
                datestamp = current_split[0]
                h_current = current_split[1]

                # calculate dH/dt
                h_diff = float(h_prev) - float(h_current)

                datastring = datestamp + "," + str(h_diff)
                returnarray.append(datastring)

            print("Converted to dH/dt. " + str(len(returnarray)) + " records long")
            return returnarray

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

            print("Timestamps converted. " + str(len(temparray)) + " records long")
            return temparray





        stationdata = []

        # load parameters from the savefile for this station
        stationdata = loadcsvfile(self.station_name, self.csvfile)

        # IF THE ARRAY IS NOT EMPTY...
        if len(self.stationdata) > 0:
            # convert the times to unix
            self.stationdata = utc2unix(self.stationdata)

            # Convert dataarray to dx/dt
            self.stationdata = calc_dHdt(self.stationdata)

            # create the 24 hr bin array. Check the max value is current. Save out if it increases

            # NOrmalise the array against the max value as stored.

            # save out station parameters

        self.stationdata = stationdata


