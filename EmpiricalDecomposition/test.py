#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 19:49:07 2018

@author: vaughn
"""

class DataPoint:
    def __init__(self, posix_dt, datavalue):
        self.null = "#n/a"
        self.maxvalue = self.null
        self.minvalue = self.null
        
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

# refine the list to the format [posix_date, datavalue]
def refine_magnetometer_data(datalist):
    returnlist = []
    datalist.pop(0)
    for item in datalist:
        datasplit = item.split(",")
        posixdate = int(float(datasplit[1]))
        datavalue = datasplit[2]
        dp = str(posixdate) + "," + str(datavalue)
        returnlist.append(dp)
    return returnlist

if __name__ == "__main__":
    magnetometer_data = loadcsv("2018-06-18.csv")
    print(magnetometer_data[0])
    magnetometer_data = refine_magnetometer_data(magnetometer_data)
    print(magnetometer_data[0])

