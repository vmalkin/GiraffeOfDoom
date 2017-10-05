import time
from datetime import datetime
import Station
import os
import unittest


station_details = (("Ruru Observatory Rapid-run magnetometer", "http://www.ruruobservatory.org.nz/dr01_1hr.csv",
                    "w3", "%Y-%m-%d %H:%M:%S.%f", 30),)

# create the list of magnetometer stations
station_list = []
for item in station_details:
    new_station = Station.Station(item)
    station_list.append(new_station)

if __name__ == "__main__":
    # while True:
    # calculate the processing time
    starttime = datetime.now()
    starttime = time.mktime(starttime.timetuple())

    # for each station.....


    # Calculate the elapsed processing time and display the result to the console...
    finishtime = datetime.now()
    finishtime = time.mktime(finishtime.timetuple())
    elapsedtime = finishtime - starttime
    elapsedtime = float(elapsedtime / 60)
    print("\nElapsed time is " + str(elapsedtime) + " minutes.")

        # time.sleep(121)