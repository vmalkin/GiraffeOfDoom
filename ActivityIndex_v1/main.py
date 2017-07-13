import time
from time import mktime
from datetime import datetime
import urllib.request as webreader
import os

NULLBIN = "#n/a"

class Station:
    def __init__(self, name, datasource, sourcetype, dateformat):
        self.name = name
        self.datasource = datasource
        self.sourcetype = sourcetype
        self.dateformat = dateformat
        self.binned_data = []

    # GET the source data
    def get_data(self):
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
            self.binned_data = importarray

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
                self.binned_data = importarray
            else:
                print("UNABLE to load data for " + self.name)

    def make_dhdt(self, rawdata):
        returnarray = []

        for i in range(1, len(rawdata)):
            olddata = rawdata[i - 1].split(",")
            nowdata = rawdata[i].split(",")

            nowtime = nowdata[0]
            dhdt = float(nowdata[1]) - float(olddata[1])
            dp = nowtime + "," + str(dhdt)

            returnarray.append(dp)

        return returnarray

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
        for i in range(1, len(self.binned_data)):
            try:
                itemsplit = self.binned_data[i].split(",")
                newdatetime = datetime.strptime(itemsplit[0], dateformat)
                # convert to Unix time (Seconds)
                newdatetime = mktime(newdatetime.timetuple())

                datastring = str(newdatetime) + "," + str(itemsplit[1])
                workingarray.append(datastring)
            except:
                count = count + 1
                print("UTC 2 Unix conversion - problem with entry " + str(count))

        self.binned_data = workingarray

    # #################################################################################
    # Rawdata is in the format (UnixDatetime, data)
    # the function will return an array of (binned_value))
    # #################################################################################
    def bin_dh_dt(self):
        # setup the bin array based on binsize. The bins will start from now and go back 24 hours
        # get current UTC
        currentdt = datetime.utcnow()

        # Convert to UNIX time
        currentdt = mktime(currentdt.timetuple())

        # width of bin in seconds.
        binwidth = 60 * 60

        # how many bins in a day?
        binnum = int(86400 / binwidth)
        print("Bin width is " + str(binwidth) + " seconds. There are " + str(binnum) + " bins in a day")

        # Threshold value for binning. We need more that this number of datapoints per bin, to have a reasonable amount
        # of data
        threshold = 1

        # setup the binneddata array timestamps
        # the array goes from index[now] -> index[time is oldest]
        timestamps = []
        for i in range(0, binnum):
            timestamps.append(currentdt)
            currentdt = currentdt - binwidth

        # array for final binned values
        binneddata = []

        # parse thru the data array, assigning the correct values to the bins
        for i in range(0, len(timestamps) - 1):
            nowtime = timestamps[i]
            prevtime = timestamps[i + 1]
            maxv = float(-1000)
            minv = float(1000)

            # GO thru the raw data and check for max-min H readings and calculate the rate of change for the bin
            for j in range(0, len(self.binned_data)):
                datasplit = self.binned_data[j].split(",")
                datadate = float(datasplit[0])
                datavalue = float(datasplit[1])

                # if the data falls into the range of the bin, determine if its a max or min value
                if datadate < nowtime and datadate > prevtime:
                    # determin max and min values for this window interval
                    if datavalue >= maxv:
                        maxv = datavalue
                    elif datavalue <= minv:
                        minv = datavalue

            # determin dH/dt for the bin period append to the bin array
            # null data will manifest as a large minus value, so we discount it
            hvalue = maxv - minv
            if hvalue < -500:
                binneddata.append(NULLBIN)
            else:
                binneddata.append(hvalue)

            self.binned_data = binneddata

    # #################################################################################
    # Save the raw datapoint array to the save file
    # #################################################################################
    def SaveRawArray(self):
        # export array to array-save file
        try:
            with open(self.name + ".csv", 'w') as w:
                for dataObjects in self.binned_data:
                    w.write(str(dataObjects) + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + self.name + ".csv")

# ###############################################
# recalculate the max min values once per 24hr
# ###############################################
def do_renormalise():
    pass

if __name__ == '__main__':
    starttime = datetime.now()
    starttime = time.mktime(starttime.timetuple())

    stationlist = []
    station1 = Station("Dalmore", "Dalmore_Prime.1minbins.csv", "f1", '%Y-%m-%d %H:%M')
    station2 = Station("DnAurora", "http://Dunedinaurora.nz/Service24CSV.php", "w1", '"%Y-%m-%d %H:%M:%S"')

    stationlist.append(station1)
    stationlist.append(station2)

    for magstation in stationlist:
        magstation.get_data()
        magstation.utc2unix()
        magstation.bin_dh_dt()
        magstation.SaveRawArray()

    # while True:
    #     #sleep time in seconds 86400sec in a day
    #     sleeptime = 900
    #     currenttime = datetime.now()
    #     currenttime = time.mktime(currenttime.timetuple())
    #
    #     if currenttime > starttime + 86400:
    #         do_renormalise()
    #         starttime = currenttime
    #     else:
    #         do_main()
    #     time.sleep(sleeptime)