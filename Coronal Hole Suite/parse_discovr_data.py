import requests
from decimal import Decimal, getcontext
getcontext().prec = 4


# #################################################################################
# GET the source data
# #################################################################################
def get_json():
    # DISCOVR satellite data in JSON format
    # first is the header values, then the data values:
    # ["time_tag","density","speed","temperature"]
    # ["2018-03-19 02:05:00.000","6.35","573.4","330513"]
  
    url = "http://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    
    try:
        # using Reequests library
        discovr_json = requests.get(url)
        discovr_json = discovr_json.json()

    except:
        print("Problem connecting to URL")
        
    return discovr_json

json_data = get_json()

#for item in json_data:
#    print(item[2])

counter = (0)
avg_density = (0)
for item in json_data:
    counter = counter + 1
    print(float(item[1]) +10)
    
avg_density = (avg_density) / (counter)

#counter = (0)
#avg_speed = (0)
#for item in json_data:
#    counter = counter + 1
#    avg_speed = float(avg_speed) + float(item[2])
#    
#avg_speed = (avg_speed) / (counter)
    
#print(str(avg_density) + " " + str(avg_speed))
