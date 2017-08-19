from datetime import datetime
from time import mktime
import os

__author__ = "Meepo"

class Station:
    def __init__(self, station_name, csvfile):

        # ####################################################################################
        # Instantiation starts here...
        # ####################################################################################
        self.csvfile = csvfile
        self.station_name = station_name

        # ####################################################################################
        # Load datadata from file
        # ####################################################################################
        def load_csv(self, datafile):
            importarray = []
            # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
            if os.path.isfile(datafile):
                with open(datafile) as e:
                    for line in e:
                        line = line.strip()  # remove any trailing whitespace chars like CR and NL
                        values = line.split(",")
                        dp = values[0] + "," + values[1]
                        importarray.append(dp)
            return importarray

        # ##################################################
        # Convert timestamps in array to Unix datatime
        # ##################################################
        def utc2unix(utc_data_array):
            # set date datatime format for strptime()
            # dateformat = "%Y-%m-%d %H:%M:%S.%f"
            # dateformat = '"%Y-%m-%d %H:%M:%S"'
            dateformat = '%Y-%m-%d %H:%M'

            # convert array datadata times to unix datatime
            workingarray = []
            count = 0
            for i in range(1, len(utc_data_array)):
                itemsplit = utc_data_array[i].split(",")
                newdatetime = datetime.strptime(itemsplit[0], dateformat)
                # convert to Unix datatime (Seconds)
                newdatetime = mktime(newdatetime.timetuple())

                datastring = str(newdatetime) + "," + str(itemsplit[1])
                workingarray.append(datastring)

            return workingarray

        # #################################################################################
        # normalise the datadata
        # #################################################################################
        def normaliseDHDT(unix_data_array):
            workingarray = []
            minvalue = 1000
            maxvalue = -1000

            # first calculate the max/min values in our datadata
            for item in unix_data_array:
                itemsplit = item.split(",")
                datadata = itemsplit[1]
                if float(datadata) > float(maxvalue):
                    maxvalue = datadata
                if float(datadata) < float(minvalue):
                    minvalue = datadata

            # now normalise the datadata
            for item in unix_data_array:
                itemsplit = item.split(",")
                datatime = itemsplit[0]
                datadata = itemsplit[1]

                newdata = (float(datadata) - float(minvalue)) / (float(maxvalue) - float(minvalue))
                newdata = datatime + "," + str(newdata)
                workingarray.append(newdata)

            return workingarray

        # ####################################################################################
        # This stuff happens when the class is instantiated
        # ####################################################################################
        #load the station datadata
        station_data = load_csv(self, self.csvfile)

        # convert their datetimes to UNIX
        station_data = utc2unix(station_data)

        # normalise their datadata
        station_data = normaliseDHDT(station_data)

        #
        self.station_data = station_data