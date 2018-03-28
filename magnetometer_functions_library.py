# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 09:36:14 2018

@author: vaughnm
"""

import datetime
import requests
import time

# THis is a library of common functions that I always seem to end up having to 
# access.

# ##########################################################################
# Load a CSV data file and return a list
# ##########################################################################
def load_csv(filename):
    # returns an array loaded from the logfile. 
    returnlist = []
    try:
        with open (filename, 'r') as f:
            for line in f:
                line = line.strip()  # remove \n from EOL
                returnlist.append(line)
    except:
        print("No logfile. Starting from scratch")
    return returnlist


# ##########################################################################
# Take a list and overwrite to a CSV data file
# ##########################################################################
def save_csv(datalist, filename):
    # Save a list to a disc file
    with open (filename, 'w') as w:
        for item in datalist:
            w.write(str(item) + '\n')


# ##########################################################################
# Get JSON data from the web
# ##########################################################################
def get_json():
    # DISCOVR satellite data in JSON format
    # first is the header values, then the data values:
    # ["time_tag","density","speed","temperature"]
    # ["2018-03-19 02:05:00.000","6.35","573.4","330513"]
  
    url = "http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json"
    response = requests.get(url)
    discovr_data = response.json()  # requests has built in json
    return discovr_data


# ##########################################################################
# Return the current UTC time STRING
# ##########################################################################            
def get_utc_time():
    # returns a STRING of the current UTC time
    # %Y-%m-%d %H:%M:%S.%f
    time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    return time_now


# ##########################################################################
# Convert a UTC time string to POSIX time
# Watch the format of the timestring
# ########################################################################## 
def utc2posix(timestamp):
    # 2018-03-19 02:05:00.000
    # %Y-%m-%d %H:%M:%S
    posix_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    posix_time = time.mktime(posix_time)
    return posix_time


# ##########################################################################
# Convert POSIX time string to a UTC time OBJECT
# ########################################################################## 
def posix2utc(timestamp):
    utctime = datetime.datetime.utcfromtimestamp(timestamp)
    return utctime
