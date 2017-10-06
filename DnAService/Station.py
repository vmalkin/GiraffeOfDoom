import time
from time import mktime
from datetime import datetime
import urllib.request as webreader
import os
import pickle

NULLBIN = "#n/a"

class Station:
    def __init__(self, station_details_tuple):
        # each item has the format ("name", "data_source", "source_type", "dateformat", readings_per_minute)
        self.name = station_details_tuple[0]
        self.datasource = station_details_tuple[1]
        self.sourcetype = station_details_tuple[2]
        self.dateformat = station_details_tuple[3]
        self.readfreq = station_details_tuple[4]

        # stationdata is the accumulating data for each minuten of the past 24 hours for this station
        self.stationdata = self.loadpickle()

    # #################################################################################
    # load pickle file and return the min-max array
    # #################################################################################
    def loadpickle(self):
        """load pickle file"""
        savefile = self.name + ".savedata.pkl"
        try:
            with open(savefile,"rb", ) as sv:
                dataarray = sv.read()
        except:
            dataarray = []
            print("No file to load. Creating values of zero")

        return dataarray

    # #################################################################################
    # save array to pickle file. Prints a result
    # #################################################################################
    def savepickle(self, datatosave):
        savefile = self.name + ".savedata.pkl"
        try:
            pickle.dump(datatosave, open(savefile, "wb"))
            print("Save " + savefile + " ok.")
        except:
            print("ERROR saving array")


    # #################################################################################
    # GET the source data
    # #################################################################################
    def get_data(self):
        # GOES Satellite Magnetometer Data - Total Field only.
        if self.sourcetype == "w2":
            url = self.datasource
            importarray = []
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

            except webreader.HTTPError as err:
                if err.code == 404:
                    print("Error 404")

            except webreader.URLError as err:
                print("There was an error associated with the URL")

            return importarray

        # Dunedin Aurora CSV data
        if self.sourcetype == "w1":
            url = self.datasource
            importarray = []
            response = webreader.urlopen(url)
            for item in response:
                logData = str(item, 'ascii').strip()
                logData = logData.split(",")
                dp = logData[0] + "," + logData[1]
                importarray.append(dp)
            print("Data for " + self.name + " loaded from Internet. Size: " + str(len(importarray)) + " records")
            return importarray

        # Ruru Observatory CSV data
        if self.sourcetype == "w3":
            url = self.datasource
            importarray = []
            response = webreader.urlopen(url)
            for item in response:
                logData = str(item, 'ascii').strip()
                logData = logData.split(",")
                dp = logData[0] + "," + logData[1]
                importarray.append(dp)
            print("Data for " + self.name + " loaded from Internet. Size: " + str(len(importarray)) + " records")
            return importarray

        # % Y-%m-%d %H:%M:%S.%f from a file (My magnetometers)
        if self.sourcetype == "f1":
            importarray = []
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

    # #################################################################################
    # APpend new data to the running array
    # #################################################################################
    def append_new_data(self):
        pass


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
            previtems = new_data[i].split(",")
            currentitems = new_data[i-1].split(",")
            currentdt = currentitems[0]

            if (currentitems[1]) == '':
                currentdata = 0
            else:
                currentdata = float(currentitems[1])

            if (previtems[1]) == '':
                prevdata = 0
            else:
                prevdata = float(str(previtems[1]))

            dadt =  currentdata - prevdata

            datastring = str(currentdt) + "," + str(dadt)
            dadtlist.append(datastring)
        return dadtlist

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
        print("ORIGINAL Data list is " + str(len(self.save_array)) + " records long")

        for i in range(0, len(self.save_array)):
        # for item in workingdatalist:
            itemlist = self.save_array[i].split(",")
            newdatetime = float(itemlist[0])

            if newdatetime > cutoffdt:
                # print(newdatetime - cutoffdt)
                workingdatalist.append(self.save_array[i])

        print("PRUNED Data list is " + str(len(workingdatalist)) + " records long")
        self.save_array = workingdatalist

    def despike(self, dataarray):
        return dataarray

    # #################################################################################
    # Save the binned data as CSV file
    # #################################################################################
    def SaveAsCSV(self, namestring):
        # export array to array-save file
        try:
            with open(namestring + ".csv", 'w') as w:
                for dataObjects in self.save_array:
                    w.write(str(dataObjects) + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + self.name + ".csv")


    # #################################################################################
    # aggregate new data onto current data
    # #################################################################################
    def aggregate_new_data(self, currentdata, newdata):
        pass


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

        # convert new data to rate of change
        new_data = self.create_dadt(new_data)
        print("Calculated dF/dt of new data for " + self.name)

        # remove spikes
        new_data = self.despike(new_data)

        # Aggregate new data onto current data array. We need to check thru the stationdata and makre sure a datetime
        # is not duplicted. We will use Set() with a union to do this.
        self.stationdata = self.aggregate_new_data(self.stationdata, new_data)

        # Prune current data to whatever length
        nowtime = datetime.now()
        nowtime = time.mktime(nowtime.timetuple())
        begintime = nowtime - (60*60*24)

        temparray = []
        for item in self.stationdata:
            itemsplit = item.split(",")
            itemdate = itemsplit[0]

            if float(itemdate) > begintime:
                temparray.append(item)
        self.stationdata = temparray
        print("Data for " + self.name + " is " + str(len(self.stationdata)) + " records long")

        # SAVE current data to PKL file
        print("Saving current data for " + self.name)
        self.savepickle(self.stationdata)

        print("\n")
