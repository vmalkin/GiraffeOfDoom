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
errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)
WIND_SPEED_THRESHOLD = 800
getcontext().prec = 6
NULL = "null"

class SatelliteDataProcessor:
    def __init__(self):
        logging.info("instantiated Satellite Data Processor")
        self.wind_density = 0
        self.wind_speed = 0
        self.satdata = []


    def _utc2posix(self, timestamp):
        # 2018-03-19 02:05:00.000
        # %Y-%m-%d %H:%M:%S
        posix_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        posix_time = time.mktime(posix_time)
        return posix_time


    def _get_json(self):
        # DISCOVR satellite data in JSON format
        # first is the header values, then the data values:
        # ["time_tag","density","speed","temperature"]
        # ["2018-03-19 02:05:00.000","6.35","573.4","330513"]
        try:
            url = "http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json"
            response = requests.get(url)
            discovr_data = response.json()  # requests has built in json
        except:
            # time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            discovr_data = "no_data"

        return discovr_data


    def _parse_json_convert_time(self, jsonfile):
        # converts the time to POSIX
        # grabs the Plasma and Density data
        # returns a python list
        returnlist = []
        for i in range(1, len(jsonfile)):
            date_posix = self._utc2posix(jsonfile[i][0])
            wind_density = jsonfile[i][1]
            wind_speed = jsonfile[i][2]

            csvdata = str(date_posix) + "," + str(wind_density) + "," + str(wind_speed)
            returnlist.append(csvdata)

        return returnlist


    def _parse_json_prune(self, posix_list):
        # we want only the data for the last hour.
        # we will return a modified array of the current data only
        nowtime = self._utc2posix(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")))
        prevtime = nowtime - 3600  # the past hour
        returnarray = []

        for i in range (1, len(posix_list)):
            datasplit = posix_list[i].split(",")
            checkdate = datasplit[0]
            wind_density = datasplit[1]
            wind_speed = datasplit[2]
            # print(str(checkdate) + " " + str(nowtime) + " " + str(prevtime))
            if float(checkdate) > float(str(prevtime)) and float(checkdate) <= float(str(nowtime)):
                csvdata = str(checkdate) + "," + str(wind_density) + "," + str(wind_speed)
                returnarray.append(csvdata)
        return returnarray


    def _plasma_density(self, posix_list):
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
            wind_density = 0
        return wind_density


    def _plasma_speed(self, posix_list):
        try:
            wind_speed = 0
            counter = 0
            for i in range(1, len(posix_list)):
                datasplit = posix_list[i].split(",")
                value = datasplit[2]
                wind_speed = wind_speed + Decimal(value)
                counter = counter + 1
            wind_speed = Decimal(wind_speed) / Decimal(counter)

            if wind_speed > WIND_SPEED_THRESHOLD:
                wind_speed = 400
        except:
            wind_speed = 0
        return wind_speed


    # ################################
    # W R A P P E R   F U N C T I O N
    # ################################
    def get_data(self):
        self.satdata = self._get_json()
        if self.satdata == "no_data":
            # Unable to get DISCOVR data
            self.plasma_density = 0
            self.plasma_speed = 0
        else:
            # parse new data to the correct format
            # The timestampt is in POSIX format
            dscvr_data = self._parse_json_convert_time(self.satdata)

            # we want only the ast hour of data
            dscvr_data = self._parse_json_prune(dscvr_data)

            # get the avg windspeed and plasma density
            self.wind_density = self._plasma_density(dscvr_data)
            self.wind_speed = self._plasma_speed(dscvr_data)
