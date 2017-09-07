import time
from time import mktime
from datetime import datetime
import urllib.request as webreader
import os
import pickle

NULLBIN = "#n/a"

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
