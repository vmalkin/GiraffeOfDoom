import requests

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

