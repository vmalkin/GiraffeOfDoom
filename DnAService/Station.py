import math
from time import mktime
from datetime import datetime
import urllib.request as webreader
from urllib.error import  URLError
import os
import pickle

NULLBIN = "#n/a"

class Station:
    def __init__(self, name, datasource, sourcetype, dateformat, readfreq, blips):
        # each item has the format ("name", "data_source", "source_type", "dateformat", readings_per_minute, blip_threshold)
        self.name = name
        self.datasource = datasource
        self.sourcetype = sourcetype
        self.dateformat = dateformat
        self.readfreq = readfreq
        self.blip_threshold = blips

        # stationdata is the accumulating data for each minuten of the past 24 hours for this station
        self.station_data_file = self.name + ".data.csv"
        self.stationdata = self.load_csv(self.station_data_file)
        self.displaylist = []


    # #################################################################################
    # GET the source data
    # #################################################################################
    def get_data(self):
        # return array
        importarray = []

        # GOES Satellite Magnetometer Data - Total Field only.
        if self.sourcetype == "w2":
            url = self.datasource
            try:
                response = webreader.urlopen(url)
                linecount = 0

                for item in response:
                    linecount = linecount + 1
                    if linecount > 21:
                        logData = str(item, 'ascii').strip()
                        logData = logData.split()
                        # print(str(logData) + " " + str(linecount))
                        dp_date = logData[0] + "-" + logData[1] + "-" + logData[2]

                        dp_time = logData[3][:2] + ":" + logData[3][2:]

                        dp_data = logData[9]
                        dp_data = dp_data.split("e")
                        dp_data = dp_data[0]

                        dp = dp_date + " " + dp_time + "," + dp_data
                        importarray.append(dp)

                print("Data for " + self.name + " loaded from Internet. Size: " + str(len(importarray)) + " records")

            except URLError as e:
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)

            # except webreader.HTTPError as err:
            #     print("A non-handled HTTP error occurred")
            #
            # except webreader.URLError as err:
            #     print("There was an error associated with the URL")


        # Dunedin Aurora CSV data
        if self.sourcetype == "w1":
            url = self.datasource
            try:
                response = webreader.urlopen(url)
                for item in response:
                    logData = str(item, 'ascii').strip()
                    logData = logData.split(",")
                    dp = logData[0] + "," + logData[1]
                    importarray.append(dp)
                print("Data for " + self.name + " loaded from Internet. Size: " + str(len(importarray)) + " records")
            except URLError as e:
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)

        # Ruru Observatory CSV data
        if self.sourcetype == "w3":
            url = self.datasource
            try:
                response = webreader.urlopen(url)
                for item in response:
                    logData = str(item, 'ascii').strip()
                    logData = logData.split(",")
                    dp = logData[0] + "," + logData[1]
                    importarray.append(dp)
                print("Data for " + self.name + " loaded from Internet. Size: " + str(len(importarray)) + " records")
            except URLError as e:
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)

        # % Y-%m-%d %H:%M:%S.%f from a file (My magnetometers)
        if self.sourcetype == "f1":
            # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
            if os.path.isfile(self.datasource):
                with open(self.datasource) as e:
                    for line in e:
                        line = line.strip()  # remove any trailing whitespace chars like CR and NL
                        values = line.split(",")
                        dp = values[0] + "," + values[1]
                        importarray.append(dp)
                print("Data for " + self.name + " loaded from File. Size: " + str(len(importarray)) + " records")
                return importarray
            else:
                print("UNABLE to load data for " + self.name)

        return importarray

    # ##################################################
    # Convert timestamps in array to UTC time
    # ##################################################
    def unix2utc(self, dataarray):
        # dateformat = "%Y-%m-%d %H:%M:%S"
        returnarray = []

        for item in dataarray:
            itemsplit = item.split(",")
            itemdate = itemsplit[0]
            itemdate = itemdate.split(".")
            itemdate = int(itemdate[0])

            itemdatavalue = itemsplit[1]
            utcdate = datetime.fromtimestamp(itemdate)

            returnitem = str(utcdate) + "," + itemdatavalue
            returnarray.append(returnitem)
        return returnarray

    # ##################################################
    # Convert timestamps in array to Unix time
    # ##################################################
    def utc2unix(self, new_data_array):
        print("Converting time to UNIX time...")

        # set date time format for strptime()
        # dateformat = "%Y-%m-%d %H:%M:%S.%f"
        # dateformat = '"%Y-%m-%d %H:%M:%S"'
        # dateformat = '%Y-%m-%d %H:%M'
        dateformat = self.dateformat

        # convert array data times to unix time
        workingarray = []

        for item in new_data_array:
            try:
                itemsplit = item.split(",")
                newdatetime = itemsplit[0]
                newdatetime = datetime.strptime(newdatetime, dateformat)
                # convert to Unix time (Seconds)
                newdatetime = mktime(newdatetime.timetuple())

                datastring = str(newdatetime) + "," + str(itemsplit[1])
                workingarray.append(datastring)
            except:
                print("UTC 2 Unix conversion - problem with entry " + str(item))
        return workingarray

    # turn raw values into rates of change
    def create_dadt(self, new_data):
        dadtlist = []

        for i in range(1, len(new_data)):
            currentsplit = new_data[i].split(",")
            currentdt = currentsplit[0]
            currentdata = float(currentsplit[1])

            prevsplit = new_data[i - 1].split(",")
            prevdata = float(prevsplit[1])

            dadt = currentdata - prevdata

            test_dadt = math.sqrt(math.pow(dadt,2))
            if test_dadt > self.blip_threshold:
                dadt = 0.0
                print("BLIP detected")

            datastring = str(currentdt) + "," + str(dadt)
            dadtlist.append(datastring)
        return dadtlist


    def rebuild_from_dadt(self, dadt_data):
        returnarray = []
        returnvalue = 0

        for i in range(0,len(dadt_data)):
            datasplit = dadt_data[i].split(",")
            datetime = datasplit[0]
            datavalue = float(datasplit[1])
            returnvalue = returnvalue + datavalue

            datastring = datetime + "," + str(returnvalue)
            returnarray.append(datastring)

        return returnarray


    def prune_saved_data(self):
        # IF NECESSARY prune the dataset BACK from the earliest bin datetime as previously determined to keep the data
        # in scope fort the current 24/48/whatever hour period
        # get current UTC
        workingdatalist = []
        currentdt = datetime.utcnow()
        currentdt = mktime(currentdt.timetuple())
        cutoffdt = float(currentdt - (24*60*60))

        print("Time now is " +  str(currentdt))
        print("Cutoff for old data is " + str(cutoffdt))
        print("ORIGINAL Data list is " + str(len(self.stationdata)) + " records long")

        for i in range(0, len(self.stationdata)):
        # for item in workingdatalist:
            itemlist = self.stationdata[i].split(",")
            newdatetime = float(itemlist[0])

            if newdatetime > cutoffdt:
                # print(newdatetime - cutoffdt)
                workingdatalist.append(self.stationdata[i])

        print("PRUNED Data list is " + str(len(workingdatalist)) + " records long")
        return workingdatalist


    # ##################################################
    # Save out CSV data
    # ##################################################
    def save_csv(self, arraydata, savefile):
        try:
            os.remove(savefile)
        except:
            print("Error deleting old file")

        for line in arraydata:
            try:
                with open(savefile, 'a') as f:
                    f.write(line + "\n")

            except IOError:
                print("WARNING: There was a problem accessing file")

    # #################################################################################
    # LOad CSV
    # #################################################################################
    def load_csv(self, loadfile):
        readings = []
        # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
        if os.path.isfile(loadfile):
            with open(loadfile) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    readings.append(line)
            print("Array loaded from file. Size: " + str(len(readings)) + " records")
        else:
            print("No save file loaded. Using new array.")

        return readings

    # #################################################################################
    # aggregate new data onto current data
    # #################################################################################
    def aggregate_new_data(self, currentdata, newdata):
        returndata = currentdata
        latestdate = 0.0

        # find the biggest datetime in the current data
        for item in currentdata:
            itemsplit = item.split(",")
            checkdate = float(itemsplit[0])

            if checkdate > latestdate:
                latestdate = checkdate

        # now check thru the new data looking for items more recent than the latest date
        for item in newdata:
            itemsplit = item.split(",")
            checkdate = float(itemsplit[0])

            # if it's later append to the return results
            if checkdate > latestdate:
                returndata.append(item)

        return returndata


    # #################################################################################
    # Wrapper function that will process new readings for this station
    # #################################################################################
    def process_mag_station(self):
        # Get new data
        # we should end up with UTCdate, datavalue
        new_data = []
        new_data = self.get_data()
        print("Loaded NEW data for " + self.name)

        # split new data and convert timestamps to UNIX
        new_data = self.utc2unix(new_data)
        print("Converted timestamps of new data for " + self.name)

        # Aggregate new data onto current data array. We need to check thru the stationdata and makre sure a datetime
        # is not duplicted. We will use Set() with a union to do this.
        self.stationdata = self.aggregate_new_data(self.stationdata, new_data)

        # pruning old data
        self.stationdata = self.prune_saved_data()

        print("Data for " + self.name + " is " + str(len(self.stationdata)) + " records long")

        # SAVE current data to csv file
        print("Saving current data for " + self.name)
        self.save_csv(self.stationdata, self.station_data_file)

        # create the display file with UTC timestamps
        displayfile = "display." + self.station_data_file
        self.stationdata = self.unix2utc(self.stationdata)
        self.save_csv(self.stationdata, displayfile)

        print("\n")
