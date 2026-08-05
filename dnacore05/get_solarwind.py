import sqlite3
import constants as k
import logging
import requests
from datetime import datetime, timezone
from calendar import timegm
import time

"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.ERROR
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
datasource = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json"
station_id = "SW_Density"
timeformat = '%Y-%m-%d %H:%M:%S.%f'

class State:
    def __init__(self):
        self.nowdate = 0
        self.initaldata = []
        self.parseddata = []

    def do_get_data(self):
        json_data = requests.get(datasource, timeout=10).json()
        for i in range(1, len(json_data)):
            time_tag = self.utc2posix(json_data[i][0])
            speed = json_data[i][1]
            density = json_data[i][2]
            bz = json_data[i][6]
            dp = [time_tag, speed, density, bz]
            self.initaldata.append(dp)


    # def do_parse_data(self):
    #     """Parse the magdata from the most recent date. Data should have format of posixtime, datavalue. """
    #     result = "fail"
    #     tempdata = []
    #     for row in self.data:
    #         row = row.split(",")
    #         # print(row)
    #         dt = int(row[0])
    #         data = row[1]
    #         if dt > int(self.nowdate):
    #             dp = str(dt) + ", " + str(data)
    #             tempdata.append(dp)
    #     if len(tempdata) > 0:
    #         self.mag_data = tempdata
    #         result = "success"
    #     print("Number of records to append: " + str(len(tempdata)))
    #     return result
    #
    # def do_most_recent_date(self):
    #     result = "success"
    #     # select max(posix_time) from station_data where station_data.station_id = "Ruru_Obs" order by posix_time asc;
    #     query_result = db.execute("select max(posix_time) from station_data where station_data.station_id = ? order by posix_time asc", [station_id])
    #     # query_result = db.execute("select max(posix_time) from station_data order by posix_time asc")
    #     tempdate = query_result.fetchone()
    #     tempdate = tempdate[0]
    #     # print(tempdate)
    #     if tempdate != None:
    #         self.nowdate = int(tempdate)
    #     else:
    #         pass
    #     print("Most recent date: " + str(self.nowdate))
    #     return result
    #
    # def do_data_append(self):
    #     """Append the magdata to the database."""
    #     result = "fail"
    #     try:
    #         for item in self.mag_data:
    #             itemsplit = item.split(",")
    #             db.execute("insert into station_data(station_id, posix_time, data_value) values (?, ?, ?)", [station_id, itemsplit[0], itemsplit[1]])
    #         result = "success"
    #     except sqlite3.ProgrammingError:
    #         print(station_id + " ERROR: Error with query")
    #         logging.error(station_id + " ERROR: Error with query")
    #     return result

    def posix2utc(posixtime, timeformat):
        # '%Y-%m-%d %H:%M'
        utctime = datetime.fromtimestamp(posixtime, tz=timezone.utc).strftime(timeformat)
        return utctime

    def utc2posix(utcstring, timeformat):
        utc_time = time.strptime(utcstring, timeformat)
        epoch_time = timegm(utc_time)
        return epoch_time

solarwind = State()
if __name__ == "__main__":
    solarwind.do_get_data()
    # solarwind.do_parse_data()
    # solarwind.do_most_recent_date()
    # solarwind.do_data_append()
