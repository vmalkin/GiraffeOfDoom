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

# This must match station entries in constants.py
station_speed = "SW_speed"
station_density = "SW_Density"
station_bz = "SW_Bz"

timeformat = '%Y-%m-%d %H:%M:%S.%f'

class State:
    def __init__(self):
        self.nowdate = 0
        self.initaldata = []
        self.parseddata = []


    def do_get_data(self):
        json_data = requests.get(datasource, timeout=10).json()
        for i in range(1, len(json_data)):
            time_tag = self.utc2posix(utcstring=json_data[i][0], timeformat='%Y-%m-%dT%H:%M:%SZ')
            speed = json_data[i][1]
            density = json_data[i][2]
            bz = json_data[i][6]
            dp = [time_tag, speed, density, bz]
            self.initaldata.append(dp)



    def do_most_recent_date(self):
        # select max(posix_time) from station_data where station_data.station_id = "Ruru_Obs" order by posix_time asc;
        query_result = db.execute("select max(posix_time) from station_data where station_data.station_id = ? order by posix_time asc", [station_bz])
        # query_result = db.execute("select max(posix_time) from station_data order by posix_time asc")
        tempdate = query_result.fetchone()
        tempdate = tempdate[0]
        # print(tempdate)
        if tempdate != None:
            self.nowdate = int(tempdate)
        else:
            pass
        print("Most recent date: " + str(self.nowdate))


    def do_parse_data(self):
        # [1785967500, 349.2, 1.36, -1.64], posixtime, speed, density, bz
        for row in self.initaldata:
            dt = int(row[0])
            if dt > int(self.nowdate):
                self.parseddata.append(row)
        print(f"Number of parsed data records: {len(self.parseddata)}")


    def do_data_append(self):
        """Append the parsed data to the database."""
        try:
            for item in self.mag_data:
                itemsplit = item.split(",")
                db.execute("insert into station_data(station_id, posix_time, data_value) values (?, ?, ?)", [station_id, itemsplit[0], itemsplit[1]])
            result = "success"
        except sqlite3.ProgrammingError:
            print(station_id + " ERROR: Error with query")
            logging.error(station_id + " ERROR: Error with query")


    def posix2utc(self, posixtime, timeformat):
        # '%Y-%m-%d %H:%M'
        utctime = datetime.fromtimestamp(posixtime, tz=timezone.utc).strftime(timeformat)
        return utctime

    def utc2posix(self, utcstring, timeformat):
        utc_time = time.strptime(utcstring, timeformat)
        epoch_time = timegm(utc_time)
        return epoch_time

solarwind = State()
if __name__ == "__main__":
    solarwind.do_get_data()
    solarwind.do_most_recent_date()
    solarwind.do_parse_data()
    solarwind.do_data_append()
