import math
from time import mktime
from datetime import datetime
import urllib.request as webreader
from urllib.error import  URLError
import os
import pickle

NULLBIN = "#n/a"

class Station:
    def __init__(self, name, datasource, sourcetype, savefilename):
        # each item has the format ("name", "data_source", "source_type", savefilename)
        self.name = name
        self.datasource = datasource
        self.sourcetype = sourcetype
        self.savefilename = savefilename

    # #################################################################################
    # GET the source data
    # #################################################################################
    def get_data(self):
        # This is what will be returned
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
    # Wrapper function that will process new readings for this station
    # #################################################################################
    def process_mag_station(self):
        # Get new data
        # we should end up with UTCdate, datavalue
        new_data = []
        new_data = self.get_data()
        print("Loaded NEW data for " + self.name)

        # SAVE current data to csv file
        print("Saving current data for " + self.name)
        self.save_csv(new_data, self.savefilename)
        print("\n")
