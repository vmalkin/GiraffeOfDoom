#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 13:05:05 2018

@author: vaughn
"""
import re
from datetime import datetime
from time import mktime


class DPsimple:
    def __init__ (self, posixdate, datavalue):
        self.posixdate = posixdate
        self.datavalue = datavalue
        
#     def __str__ (self):
#        return self.posixdate + "," + self.datavalue
        
        
# Gets data from source, returns CSV list [utc_date, data, data, etc]
def get_csv_data():
    returndata = [] 
    returndata.append("Date/Time (UTC), Raw X, Raw Y, Raw Z")
    returndata.append("2018-08-03 00:00:20.94,68.676,0,0")
    returndata.append("2018-08-03 00:00:36.03,68.654,0,0")
    returndata.append("2018-08-03 00:00:51.10,68.647,0,0")
    returndata.append("2018-0t8-03 00:01:06.18,68.771,0,0")
    returndata.append("2018-0ytujr8-03 00:01:21.25,68.944,0,0")
    returndata.append("2018-08-03 00:01:36.34,68.800,0,0")
    returndata.append("2018-08-03 00:01:51.41,68.661,0,0")
    returndata.append("2018-08-03 00:02:06.49,68.943,0,0")
    returndata.append("2018-08-03 00:02:21.58,68.671,0,0")
    returndata.append("2018-08-03 00:02:36.65,68.793,0,0")
    returndata.append("2018-08-03 00:02:51.72,68.908,0,0")
    returndata.append("2018-08-03 00:03:06.80,68.814,0,0")
    return returndata

# parse thru list and return [utc_date, data] only
def clean_csv_data(raw_csv_list):
    returnlist = []
    # Ignore the first line as it should contain the header
    for i in range(1, len(raw_csv_list)):
        datasplit = raw_csv_list[i].split(",")
        datavalue = datasplit[1]
        datetime = datasplit[0]
        dp = datetime + "," + datavalue
        returnlist.append(dp)
    return returnlist

def check_valid_utc(raw_csv_list, regex, dateformat):
    returnlist = []
    errorcount = 0
    for item in raw_csv_list:
        itemsplit = item.split(",")
        utcdate = itemsplit[0]

        if re.match(regex, utcdate):
            returnlist.append(item)
        else:
            errorcount = errorcount + 1
    print(str(errorcount) + " errors in datetime encountered")
    return returnlist
    
def utc_to_posix(utcdate, formatstring):
    newdatetime = datetime.strptime(utcdate, formatstring)
    newdatetime = mktime(newdatetime.timetuple())
    newdatetime = int(newdatetime)
    return newdatetime

def create_object_list(clean_csv, formatstring): 
    return_object_list = []    
    for item in clean_csv:
        datasplit = item.split(",")
        datetime = datasplit[0]
        datavalue = datasplit[1]
        posixvalue = utc_to_posix(datetime, formatstring)
        dp = DPsimple(posixvalue, datavalue)
        return_object_list.append(dp)
    return return_object_list

# ##################################################
# median filter this works on a CSV list [datetime, data]
# ##################################################
def medianfilter(datalist):
    returnlist = []
    for i in range(1, len(datalist) - 1):
        templist = []
        datasplit_v1 = datalist[i - 1].split(",")
        datasplit_v2 = datalist[i].split(",")
        datasplit_v3 = datalist[i + 1].split(",")

        v1 = datasplit_v1[1]
        v2 = datasplit_v2[1]
        datetime = datasplit_v2[0]
        v3 = datasplit_v3[1]

        templist.append(v1)
        templist.append(v2)
        templist.append(v3)
        templist.sort()

        datavalue = templist[1]
        dp = datetime + "," + datavalue

        returnlist.append(dp)
    return returnlist

#def dhdt(objectlist):
#    returnlist = []
#    for i in range(1, len(objectlist)):
#        datetime = objectlist[i].posixdate
#        datavalue = float(objectlist[i].datavalue - float(objectlist[i-1].datavalue)
#        dp = DPsimple(datetime, datavalue)
#        returnlist.append(dp)
#    return returnlist

# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
# Data format is a list of DP_Plain objects
# #################################################################################
def running_average(input_array, averaging_interval):
    displayarray = []
    if len(input_array) > averaging_interval:
        for i in range(averaging_interval + 1, len(input_array)):
            datavalue = 0
            datetime = input_array[i].posixdate
            for j in range(0, averaging_interval):
                newdata = input_array[i-j].datavalue
                datavalue = float(datavalue) + float(newdata)

            datavalue = round((datavalue / averaging_interval), 3)
            appendvalue = DPsimple(datetime, datavalue)
            displayarray.append(appendvalue)
            print("Smoothing: "+ str(i) + " / " + str(len(input_array)))
    return displayarray


if __name__ == "__main__":
    # this could run on a while loop
    regex = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d)'
    dateformat = "%Y-%m-%d %H:%M:%S.%f"
    raw_csv_list = get_csv_data()
    
    # clean the data up
    clean_data = check_valid_utc(raw_csv_list, regex, dateformat)
    clean_data = clean_csv_data(clean_data)
    clean_data = medianfilter(clean_data)
   
    # Create the object list
    object_list = create_object_list(clean_data, dateformat)
    dhdt_list = object_list
    # Convert to dH/dt, then smooth.
#    dhdt_list = dhdt(object_list)
    dhdt_list = running_average(dhdt_list, 2)
    dhdt_list = running_average(dhdt_list, 2)