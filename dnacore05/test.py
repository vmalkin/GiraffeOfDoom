import requests

datasource = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json"
webdata = requests.get(datasource, timeout=10).json()

for i in range(1, len(webdata)):
    print(webdata[i])
