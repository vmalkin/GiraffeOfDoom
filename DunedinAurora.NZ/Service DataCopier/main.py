#!/usr/bin/env python
"""
This module is designed to aggregate data from disparate sources, and create a single aggregated CSV file to be
used by the website to display and graph. The rational for this:
1) Separation of concerns between web pages and SQL server and related performance issues, effects.
2) Aggregate data from multiple sources to provide redundancy and enable continuous service to users should any one
   magnetometer device fail.
3) Create aggregated index of hourly activity using data-merging principles that will be more useful to website users
"""

import time
import datetime
import Station
import os

__version__ = "0.9"
__author__ = "Vaughn Malkin"


# setup dictionary of stations
station_list = []

station3 = Station.Station("Ruru Observatory", "http://www.ruruobservatory.org.nz/shortdiffs.csv", "w3", "shortdiffs.csv")
station_list.append(station3)


# ############################################
# Main method starrts here
# ############################################
if __name__ == "__main__":
    while True:
        # calculate the processing time
        sleeptime = 15 * 60  # delay the next iteration
        starttime = datetime.datetime.now()
        starttime = time.mktime(starttime.timetuple())

        # for each station.....
        for mag_station in station_list:
            mag_station.process_mag_station()


        # Calculate the elapsed processing time and display the result to the console...
        finishtime = datetime.datetime.now()
        finishtime = time.mktime(finishtime.timetuple())
        elapsedtime = finishtime - starttime

        # elapsedtime = float(elapsedtime / 60)
        print("\nCOMPLETED. Time to process data was " + str(elapsedtime) + " seconds")

        for i in range(0, sleeptime):
            print(str(sleeptime - i) + " seconds until next pass")
            time.sleep(1)
