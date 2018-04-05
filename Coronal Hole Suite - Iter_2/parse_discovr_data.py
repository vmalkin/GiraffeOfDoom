import requests
from decimal import Decimal, getcontext
import time
import datetime
import logging

# setup error logging
# logging levels in order of severity:
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

getcontext().prec = 6
NULL = "null"

# #################################################################################
# Gets json data. 
# #################################################################################
def get_json():
    # DISCOVR satellite data in JSON format
    # first is the header values, then the data values:
    # ["time_tag","density","speed","temperature"]
    # ["2018-03-19 02:05:00.000","6.35","573.4","330513"]
    try:
        url = "http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json"
        response = requests.get(url)
        discovr_data = response.json()  # requests has built in json
    except:
#        time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        discovr_data = "no_data"

    return discovr_data


def parse_json_convert_time(jsonfile):
    # converts the time to POSIX
    # grabs the Plasma and Density data
    # returns a python list
    returnlist = []
    for i in range(1, len(jsonfile)):
        date_posix = utc2posix(jsonfile[i][0])
        wind_density = jsonfile[i][1]
        wind_speed = jsonfile[i][2]
        
        csvdata = str(date_posix) + "," + str(wind_density) + "," + str(wind_speed)
        returnlist.append(csvdata)
        
    return returnlist
 
           
def parse_json_prune(posix_list):
    # we want only the data for the last hour.
    # we will return a modified array of the current data only
    nowtime = utc2posix(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"))) 
    prevtime = nowtime - 3600  # the past hour
    returnarray = []
    
    for i in range (1, len(posix_list)):
        datasplit = posix_list[i].split(",")
        checkdate = datasplit[0]
        wind_density = datasplit[1]
        wind_speed = datasplit[2]
#        print(str(checkdate) + " " + str(nowtime) + " " + str(prevtime))
        if float(checkdate) > float(str(prevtime)) and float(checkdate) <= float(str(nowtime)):
            csvdata = str(checkdate) + "," + str(wind_density) + "," + str(wind_speed)
            returnarray.append(csvdata)
    return returnarray

    
def plasma_density(posix_list):
    try:
        wind_density = 0
        counter = 0
        for i in range(1, len(posix_list)):
            datasplit = posix_list[i].split(",")
            value = datasplit[1]
            wind_density = wind_density + Decimal(value)
            counter = counter + 1
            
        wind_density = Decimal(wind_density) / Decimal(counter)
    except:
        wind_density = NULL
    return wind_density


def plasma_speed(posix_list):
    try:
        wind_speed = 0
        counter = 0
        for i in range(1, len(posix_list)):
            datasplit = posix_list[i].split(",")
            value = datasplit[2]
            wind_speed = wind_speed + Decimal(value)
            counter = counter + 1
        logging.debug("Sum of windspeed: "  + str(wind_speed))
        logging.debug("counter: " + str(counter))

        wind_speed = Decimal(wind_speed) / Decimal(counter)
    except:
        wind_speed = NULL
    return wind_speed


def utc2posix(timestamp):
    # 2018-03-19 02:05:00.000
    # %Y-%m-%d %H:%M:%S
    posix_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    posix_time = time.mktime(posix_time)
    return posix_time


def posix2utc(timestamp):
    pass