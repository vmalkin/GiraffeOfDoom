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

            print("Data normalised. " + str(len(temp_array)) + " records long")
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

            print("Timestamps converted. " + str(len(temparray)) + " records long")
            return temparray

        # ####################################################################################
        # converts the UTC timestamp to unix time. returns converted array.
        # ####################################################################################
        def unix2utc(dataarray):
            temparray = []

            # For each item in the submitted array...
            for item in dataarray:
                # Split and get the unix date from the actual data
                item = item.split(",")
                unixdate = item[0]
                arraydata = item[1]

                # Convert the unix date to UTC time
                utctime = datetime.datetime.fromtimestamp(int(unixdate)).strftime("%Y-%m-%d %H:%M")

                # Recombine with the data and append to the array to be returned. Voila!
                appenddata = str(utctime) + "," + arraydata
                temparray.append(appenddata)

            return temparray

        # #################################################################################
        # Median filter based on 3 values
        # Array is datetime,value
        # #################################################################################
        def median_filter_3values(arraydata):
            # set up the return array
            returnarray = []

            # Parse thru the arraydata
            for i in range(1,len(arraydata) - 1):
                hsort = []

                # get the unix timestamp
                datasplit = arraydata[i].split(",")
                datestamp = datasplit[0]

                # for each i, grab the data before, i, and data after, append the the sort array
                for j in range(-1,2):
                    datasplit = arraydata[i + j].split(",")
                    hsort.append(datasplit[1])
                # sort
                hsort.sort()

                #grab the middlemost data and append to the return array
                datastring = datestamp + "," + hsort[1]
                returnarray.append(datastring)

            print("Median filter applied. " + str(len(returnarray)) + " records long")
            return returnarray

        # #################################################################################
        # Create the smoothed data array and write out the files for plotting.
        # We will do a running average based on the running average time in minutes and the number
        # readings per minute
        #
        # we will divide this number evenly so our average represents the midpoint of these
        # readings.
        # #################################################################################
        def running_average(input_array):
            # set up the return array
            returnarray = []

            # Parse thru the arraydata
            for i in range(2, len(input_array) - 2):
                # get the unix timestamp
                datasplit = input_array[i].split(",")
                datestamp = datasplit[0]

                hvalue = 0
                # for each i, grab the data before, i, and data after, append the the sort array
                for j in range(-2, 3):
                    datasplit = input_array[i + j].split(",")
                    hvalue = float(hvalue) + float(datasplit[1])

                hvalue = hvalue / 5

                # grab data and append to the return array
                datastring = datestamp + "," + str(hvalue)
                returnarray.append(datastring)

            print("Running average applied. " + str(len(returnarray)) + " records long")
            return returnarray

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
        # Create array of dH/dt binned by hours
        # ####################################################################################
        def hourbins(h_diffs):
            returnarray = []
            # calculate how many hours are in the present data array. Create a new readings array
            # prepopulated with corresponding timestamps
            starttime = h_diffs[0].split(",")
            endtime = h_diffs[len(h_diffs) - 1].split(",")
            starttime = int(float((starttime[0])))
            endtime = int(float(endtime[0]))


            # Is our incoming array big enough? AT least one hour of data to start with
            if (endtime - starttime) > 3660:

                # We are going to count backwards, so that we go back in whole hours. Add the timestamps
                timestamps = []
                i = endtime

                while i > starttime:
                    timestamps.append(i)
                    i = i - 3660

                timestamps.append(starttime)

                # flip them back around the right way
                timestamps.reverse()

                # What we want to do now is to use the values stored in timestamps to find the max/min values
                # in our data and calculate the differences accordingly

                # Use the timestamps array to calculate the limits for the hour
                for i in range(1, len(timestamps)):
                    beginhour = timestamps[i - 1]
                    endhour = timestamps[i]
                    maxh = float(-10000)
                    minh = float(10000)
                    diffdata = 0

                    # now parse thru the h_diffs data, using the timestamp limits to find dH/dt for each hour
                    for j in range(0, len(h_diffs)):
                        datasplit = h_diffs[j].split(",")
                        h_diffs_date = datasplit[0]
                        h_diffs_info = datasplit[1]

                        # if we're inside the hour
                        if int(float(h_diffs_date)) >= beginhour and int(float(h_diffs_date)) < endhour:
                            if float(h_diffs_info) <= float(minh):
                                minh = h_diffs_info
                            elif float(h_diffs_info) > float(maxh):
                                maxh = h_diffs_info

                    diffdata = float(maxh) - float(minh)
                    # print(str(endhour) + " " + str(maxh) + " " + str(minh))
                    appenddata = str(endhour) + "," + str(diffdata)

                    returnarray.append(appenddata)

            print("Binned dH/dt. " + str(len(returnarray)) + " records long")
            return returnarray

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
            print("Array values inverted. " + str(len(returnarray)) + " records long")
            return returnarray

        # #################################################################################
        # Check dates
        # make sure the station dates fall inside the correct values.
        # #################################################################################
        def checkdates(data_array, nowtimevalue):
            returnarray = []
            starttime = nowtimevalue - 86400

            for i in range(0, len(data_array)):
                datasplit = data_array[i]
                if float(datasplit[0]) >= starttime and float(datasplit[0]) < nowtimevalue:
                    returnarray.append(data_array[i])

            return returnarray

        # #################################################################################
        # what is time?
        # returns the time as a unix timestamp.
        # #################################################################################
        def whatistime():
            dt = datetime.datetime.utcnow()
            unixtime = time.mktime(dt.timetuple())
            return unixtime

# ####################################################################################
# Instantiation starts here...
# ####################################################################################
        self.csvfile = csvfile
        self.station_name = station_name

        nowtimevalue = whatistime()

        # process in the station datafile
        stationdata = loadcsvfile(self.station_name, self.csvfile)

        # COnvert data timestamps to Unix time.
        stationdata = utc2unix(stationdata)

        #Check that the stationdata falls inside the correct daterange: now() minus 24 hours
        stationdata = checkdates(stationdata, nowtimevalue)

        # COnvert to H values ie: we only want the first data value a datapoint may have in this instance.
        # Datapoints that have 3 values may need to be converted to a single value here
        stationdata = producehvalues(stationdata)

        # # Normalise the data between 1 and 0
        # stationdata = normalisehvalues(stationdata)

        # Take the raw H values. SMooth them
        stationdata = running_average(stationdata)

        # Take the smoothes H values. Calculate dH/dt. Return this diffs array
        stationdata = calc_dHdt(stationdata)

        # Take the diffs array. Calculate the max differences between biggest and smallest value for each hour. Return
        # this binned data (Array of 24 values, for each of the last 24 hours)
        stationdata = hourbins(stationdata)

        #FInally, revert unix time back to UTC
        stationdata = unix2utc(stationdata)

        # Make available
        self.stationdata = stationdata

        # A station can report the begin and end times of it's data.
        begintime = self.stationdata[0]
        begintime = begintime.split(",")
        self.begintime = begintime[0]

        endtime = self.stationdata[len(stationdata) - 1]
        endtime = endtime.split(",")
        self.endtime = endtime[0]