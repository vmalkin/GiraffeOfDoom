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
    def utc2unix(self, utc_data_array):
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
    def normaliseDHDT(self, unix_data_array):
        workingarray = []

        # first calculate the max/min values in our datadata
        temp1 = []
        for i in range(1,len(unix_data_array)):
            itemsplit = unix_data_array[i].split(",")
            datavalue = itemsplit[1]
            temp1.append(datavalue)

        minvalue = float(temp1[0])
        for i in range(0,len(temp1)):
            if float(temp1[i]) <= minvalue:
                minvalue = float(temp1[i])

        maxvalue = float(temp1[0])
        for i in range(0, len(temp1)):
            if float(temp1[i]) >= maxvalue:
                maxvalue = float(temp1[i])

        # print(str(self.station_name) + ' min/max values are ' + str(minvalue) + " " + str(maxvalue))


        # now normalise the datadata
        for item in unix_data_array:
            itemsplit = item.split(",")
            datatime = itemsplit[0]
            datadata = itemsplit[1]

            newdata = (float(datadata) - float(minvalue)) / (float(maxvalue) - float(minvalue))
            newdata = datatime + "," + str(newdata)
            workingarray.append(newdata)

        testarray = []
        for item in workingarray:
            itemsplit = item.split(",")
            testarray.append(str(itemsplit[1]))
        testarray.sort()
        print(str(self.station_name) + ' NORMALISED min/max values are ' + str(testarray[0]) + " " + str(testarray[len(testarray) - 1]))

        return workingarray

    def process_stationdata(self):
        #load the station datadata
        station_data = self.load_csv(self, self.csvfile)

        # convert their datetimes to UNIX
        station_data = self.utc2unix(station_data)

        # normalise their datadata
        station_data = self.normaliseDHDT(station_data)