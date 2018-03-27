import requests
from decimal import Decimal, getcontext
import time

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
  
    url = "http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json"
    response = requests.get(url)
    discovr_data = response.json()  # requests has built in json

    return discovr_data


def parse_json_convert_time(jsonfile):
    # converts the time to POSIX
    # grabs the Plasma and Density data
    for i in range(1, len(jsonfile)):
            datetime_UTC = utc2posix(jsonfile[i][0])
            wind_density = jsonfile[i][1]
            wind_speed = jsonfile[i][2]
 
           
def parse_json_prune(posix_jsonfile):
    # we want only the data for the last hour.
    # we will return a modified array of the current data only
    nowtime = time.time()
    prevtime = nowtime - 3600  # the past hour
    returnarray = []
    
    for i in range (1, len(posix_jsonfile)):
        
    
def plasma_density(jsonfile):
    try:
        wind_density = 0
        counter = 0
        for i in range(1, len(jsonfile)):
            value = jsonfile[i][1]
            wind_density = wind_density + Decimal(value)
            counter = counter + 1
            
        wind_density = Decimal(wind_density) / Decimal(counter)
    except:
        wind_density = NULL
    return wind_density


def plasma_speed(jsonfile):
    try:
        wind_speed = 0
        counter = 0
        for i in range(1, len(jsonfile)):
            value = jsonfile[i][2]
            wind_speed = wind_speed + Decimal(value)
            counter = counter + 1
            
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
    # 1521378300.0
    
    