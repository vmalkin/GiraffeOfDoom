import datetime
import time
import os
from decimal import Decimal

__author__ = "Meepo"

class Station:
    def __init__(self, station_name, csvfile):

        FIELD_CORRECTION = 1

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
                        dp = line
                        datapointarray.append(dp)
                print("Array for " + station_name + " created, " + str(len(datapointarray)) + " records long")

                return datapointarray
            else:
                print("Unable to create list of observations for station " + self.station_name)

        # ####################################################################################
        # create and return a list/array of H values.
        # ####################################################################################
        def producehvalues(datapointarray):
            # produce an array of "H" values
            output_h = []

            # for i in range(0,len(datapointarray)):
            for line in datapointarray:
                datasplit = line.split(",")
                datetime = datasplit[0]
                datavalue = datasplit[1]
                valuestring = datetime + "," + datavalue
                output_h.append(valuestring)

            return output_h

        # ####################################################################################
        # Normalises and returns H values between 1 and 0
        # ####################################################################################
        def normalisehvalues(output_f):
            # Normalise single value data
            temp_array = []
            datamin = Decimal(0)

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
        # Smooth data
        # ####################################################################################
        def smoothdata(h_values):
            pass

        # #################################################################################
        # Median filter based on 3 values
        #
        # #################################################################################
        def median_filter_3values(arraydata):
            pass

        # #################################################################################
        # Create the smoothed data array and write out the files for plotting.
        # We will do a running average based on the running average time in minutes and the number
        # readings per minute
        #
        # we will divide this number evenly so our average represents the midpoint of these
        # readings.
        # #################################################################################
        def running_average(input_array):
            pass

        # ####################################################################################
        # Calculate diffs - dH/dt
        # ####################################################################################
        def calc_dHdt(h_values):
            pass

        # ####################################################################################
        # Create array of dH/dt binned by hours
        # ####################################################################################
        def hourbins(h_values):
            pass

        # #################################################################################
        # data inverter
        # If necessary, invert the data so that trends up mean increasing field strength
        # #################################################################################
        def invert_data_array(data_array):
            returnarray = []
            for line in data_array:
                datasplit = line.split(",")
                datetime = datasplit[0]

                x = datasplit[1] * FIELD_CORRECTION
                y = datasplit[2] * FIELD_CORRECTION
                z = datasplit[3] * FIELD_CORRECTION
                dp = datetime + "," + x + "," + y + "," + z

                returnarray.append(dp)

            return returnarray

# ####################################################################################
# Instantiation starts here...
# ####################################################################################
        self.csvfile = csvfile
        self.station_name = station_name

        # process in the station datafile
        stationdata = loadcsvfile(self.station_name, self.csvfile)

        # COnvert to H values ie: we only want the first data value a datapoint may have in this instance.
        # Datapoints that have 3 values may need to be converted to a single value here
        stationdata = producehvalues(stationdata)

        # # Normalise the data between 1 and 0
        # stationdata = normalisehvalues(stationdata)

        # COnvert data timestamps to Unix time. Make accessible self.
        stationdata = utc2unix(stationdata)

        # Take the raw H values. SMooth them

        # Take the smoothes H values. Calculate dH/dt. Return this diffs array

        # Take the diffs array. Calculate the max differences between biggest and smallest value for each hour. Return
        # this binned data (Array of 24 values, for each of the last 24 hours)

        # Make available
        self.stationdata = stationdata

        # A station can report the begin and end times of it's data.
        begintime = self.stationdata[0]
        begintime = begintime.split(",")
        self.begintime = begintime[0]

        endtime = self.stationdata[len(stationdata) - 1]
        endtime = endtime.split(",")
        self.endtime = endtime[0]



