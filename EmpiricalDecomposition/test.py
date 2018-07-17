#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:49:07 2018

@author: vaughn
"""

class DataPoint:
    def __init__(self, posix_dt, datavalue):
        self.null = "#n/a"
        self.posixdate = posix_dt
        self.datavalue = datavalue
        self.maxvalue = self.null
        self.minvalue = self.null

    def print_data(self):
        datastring = str(self.posixdate) + "," + str(self.minvalue) + "," + str(self.datavalue) + "," + str(self.maxvalue)
        return datastring
        
# Function to load CSV. Returns a list    
def loadcsv(csvfilename):
    """
    Load a CSV file.
    """
    returnlist = []
    with open(csvfilename, "r") as f:
        for line in f:
            line = line.strip()
            returnlist.append(line)
    return returnlist

# Function to load CSV. Returns a list
def savecsv(csvfilename, object_list):
    """
    Save a CSV file.
    """
    returnlist = []
    with open(csvfilename, "w") as f:
        for item in object_list:
            datastring = str(item.print_data()) + "\n"
            f.write(datastring)

# refine the list to the format [posix_date, datavalue]
def refine_magnetometer_data(datalist):
    # List to be returned
    returnlist = []

    # the positions in the datasplit for the date and data values
    index_date = 1
    index_data = 2
    datalist.pop(0)

    for item in datalist:
        datasplit = item.split(",")
        posixdate = int(float(datasplit[index_date]))
        datavalue = datasplit[index_data]
        dp = str(posixdate) + "," + str(datavalue)
        returnlist.append(dp)
    return returnlist

def list_to_object(datalist):
    returnvalue = []
    for item in datalist:
        datasplit = item.split(",")
        posixdate = datasplit[0]
        datavalue = datasplit[1]

        dp = DataPoint(posixdate, datavalue)
        returnvalue.append(dp)
    return returnvalue


def data_minmax(object_list):
    for i in range(1, len(object_list) - 1):
        prev = object_list[i-1].datavalue
        now = object_list[i].datavalue
        next = object_list[i + 1].datavalue

        if now > prev and now > next:
            object_list[i].maxvalue = now

        if now < prev and now < next:
            object_list[i].minvalue = now


if __name__ == "__main__":
    # load the data
    magnetometer_data = loadcsv("2018-06-18.csv")

    # refine data down to [posixdate, datavalue]
    magnetometer_data = refine_magnetometer_data(magnetometer_data)

    # Convert datalist to object list
    magnetometer_data = list_to_object(magnetometer_data)

    # Identify the high and low points
    data_minmax(magnetometer_data)

    # save out the CSV for diagnostic purposes
    savecsv("savefile.csv", magnetometer_data)


