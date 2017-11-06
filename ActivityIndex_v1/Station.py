import time
from time import mktime
from datetime import datetime
import urllib.request as webreader
import os
import pickle

NULLBIN = "#n/a"

class Station:
    def __init__(self, name, datasource, sourcetype, dateformat, readfreq):
        # Station name
        self.name = name

        # string for datasource - URL, filepath, etc
        self.datasource = datasource

        # Used to determin how get_data() will behave
        self.sourcetype = sourcetype

        # Date format regex for conversion
        self.dateformat = dateformat

        # how many readings per minute the data is
        self.readfreq = readfreq

        # load up previous saved data
        self.save_array = self.loadpickle()

        # min data has the format [currentmin, counter]. We increment each one
        # and calculate the avg to scale our binned data against
        self.mindata = self.loadminvalues()
        print("Current min values stored are: " + str(self.mindata[0]) + " " + str(self.mindata[1]))

        # the latest data to be downloaded
        self.latest_data = []

        # DHDT data
        self.dadt = []

        # Binned DHDT data.
        self.bin_dadt = []

    # #################################################################################
    # load pickle file and return the min-max array
    # #################################################################################
    def loadminvalues(self):
        savefile = self.name + ".minvalues.pkl"
        try:
            dataarray = pickle.load(open(savefile, "rb"))
            # print("Loaded values from file")
        except:
            dataarray = [0.001,1]
            print("No min values to load. Creating values of zero")

        return dataarray

    # #################################################################################
    # lSave the the min-max array
    # #################################################################################
    def saveminvalues(self):
        savefile = self.name + ".minvalues.pkl"
        try:
            pickle.dump(self.save_array, open(savefile, "wb"))
            print("Save " + savefile + " ok.")
        except:
            print("ERROR saving minmax values array")



    # #################################################################################
    # load pickle file and return the min-max array
    # #################################################################################
    def loadpickle(self):
        savefile = self.name + ".savedata.pkl"
        try:
            dataarray = pickle.load(open(savefile, "rb"))
            # print("Loaded values from file")
        except:
            dataarray = []
            print("No file to load. Creating values of zero")

        return dataarray

    # #################################################################################
    # save array to pickle file. Prints a result
    # #################################################################################
    def savepickle(self):
        savefile = self.name + ".savedata.pkl"
        try:
            pickle.dump(self.save_array, open(savefile, "wb"))
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

            self.latest_data = importarray

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
            self.latest_data = importarray

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
                self.latest_data = importarray
            else:
                print("UNABLE to load data for " + self.name)

    # #################################################################################
    # APpend new data to the running array
    # #################################################################################
    def append_new_data(self):
        # If we have saved data...
        if len(self.save_array) > 0:
            # get the latest item from the saved data, split on commas
            datasplit = self.save_array[len(self.save_array) - 1].split(",")
            # get the time of the latest readings. (SHould be in UNIX time.)
            latestreadingtime = datasplit[0]

            # now, for each item in the latest data fot this station...
            for item in self.latest_data:
                datasplit = item.split(",")

                # Find there the timestamp is just after the latest item in what we have already saved for
                # this station, and start appending this to our data for THIS station.
                if datasplit[0] > latestreadingtime:
                    self.save_array.append(item)
                    # print("Appended data item " + item)
        else:
            print("No saved data array")
            self.save_array = self.latest_data


    # ##################################################
    # Convert timestamps in array to Unix time
    # ##################################################
    def utc2unix(self):
        print("Converting time to UNIX time...")

        # set date time format for strptime()
        # dateformat = "%Y-%m-%d %H:%M:%S.%f"
        # dateformat = '"%Y-%m-%d %H:%M:%S"'
        # dateformat = '%Y-%m-%d %H:%M'
        dateformat = self.dateformat

        # convert array data times to unix time
        workingarray = []
        count = 0
        for i in range(1, len(self.latest_data)):
            try:
                itemsplit = self.latest_data[i].split(",")
                newdatetime = datetime.strptime(itemsplit[0], dateformat)
                # convert to Unix time (Seconds)
                newdatetime = mktime(newdatetime.timetuple())

                datastring = str(newdatetime) + "," + str(itemsplit[1])
                workingarray.append(datastring)
            except:
                count = count + 1
                print("UTC 2 Unix conversion - problem with entry " + str(count) + " " + str(self.latest_data[i]))

        self.latest_data = workingarray

    # turn raw values into rates of change
    def create_dadt(self):
        self.dadt = []
        for i in range(1, len(self.save_array)):
            previtems = self.save_array[i].split(",")
            currentitems = self.save_array[i-1].split(",")
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
            self.dadt.append(datastring)


    # #################################################################################
    # Rawdata is in the format (UnixDatetime, data)
    # the function will return an array of (binned_value))
    # #################################################################################
    def do_bin_dh_dt(self):
        pass

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
    # Calculate the average reading
    # #################################################################################
    def get_average_reading(self):
        temparray = []

        self.bin_dhdt = temparray

    # #################################################################################
    # normalise the data. The final binned data will be expressed in terms of the average minimum value
    # self.dadt is made up of absolute values.
    # #################################################################################
    def normaliseDHDT(self):
        pass

