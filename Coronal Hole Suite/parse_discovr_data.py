import requests
from decimal import Decimal, getcontext
getcontext().prec = 6


# #################################################################################
# GET the source data
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

def plasma_density(jsonfile):
    wind_density = 0
    counter = 0
    for i in range(1, len(jsonfile)):
        value = jsonfile[i][1]
        wind_density = wind_density + Decimal(value)
        counter = counter + 1
        
    wind_density = Decimal(wind_density) / Decimal(counter)
    return wind_density

def plasma_speed(jsonfile):
    wind_speed = 0
    counter = 0
    for i in range(1, len(jsonfile)):
        value = jsonfile[i][2]
        wind_speed = wind_speed + Decimal(value)
        counter = counter + 1
        
    wind_speed = Decimal(wind_speed) / Decimal(counter)
    return wind_speed

def check_timestamp(posix_time_value):
    pass

#data = get_json()
#w_dens = plasma_density(data)
#w_spd = plasma_speed(data)
#
#print(str(w_spd) + "," + str(w_dens))
    