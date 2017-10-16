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
# station0 = Station.Station("DunedinAurora.NZ", "http://Dunedinaurora.nz/Service24CSV.php", "w1", '"%Y-%m-%d %H:%M:%S"', 6, 5)
# station_list.append(station0)

station1 = Station.Station("Ruru Observatory", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30, 0.5)
station_list.append(station1)

station2 = Station.Station("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt", "w2", '%Y-%m-%d %H:%M', 1, 0.1)
station_list.append(station2)


# ##################################################
# F U N C T I O N S
# ##################################################

def create_one_minute_bin_values():
    # what is the current datetime? create a UNix timetuple
    nowtime = datetime.datetime.utcnow()
    nowtime = time.mktime(nowtime.timetuple())

    # create the list of time values for the past 24 hours
    bins = []
    for i in range(0, 1441):  # one min bins
        bins.append(nowtime)
        nowtime = nowtime - 60
    # reverse so the most recent data is last
    bins.reverse()
    return bins


# take in a datalist and two time values, output an average value for whatever data falls in-between the time range
def create_binned_data(prev_time, next_time, datalist):
    # data list has the format: unix_datetime, data
    tempstore = 0
    counter = 0
    for i in range(0, len(datalist)):
        datasplit = datalist[i].split(",")
        date_to_check = float(datasplit[0])
        data_to_add = datasplit[1]

        if date_to_check >= prev_time and date_to_check < next_time:
            tempstore = tempstore + float(data_to_add)
            counter += 1

    if tempstore == 0:
        bin_value = 0
    else:
        bin_value = float(tempstore / counter)

    return bin_value


def create_aggregated_magnetometer_values(stationlist):
    time_bins = create_one_minute_bin_values()
    finaloutput = []
    null_value = "#n/a"

    print("number of stations: " + str(len(stationlist)))
    # For each station, we need to check off what values it has that fall into our time bins, calculate the
    # average of that and append it to the final output file that will be used by the website.

    # For each time bin
    for i in range(1, len(time_bins)):
        time_prev = time_bins[i-1]
        time_now = time_bins[i]
        aggregateddata = ""

        # process each station
        for station in stationlist:
            tempdata = float(0)
            counter = 0
            # for each item in the stations DISPLAY LIST!
            for item in station.displaylist:
                datasplit = item.split(",")
                date_part = float(datasplit[0])
                data_part = datasplit[1]
                # check that it falls insode the bin range
                if date_part >= time_prev and date_part < time_now:
                    tempdata = tempdata + float(data_part)
                    counter = counter + 1
            # if we have accrued data, calculate the avg, otherwise its  null
            if tempdata > 0:
                tempdata = float(tempdata / counter)
            else:
                tempdata = null_value

            aggregateddata = aggregateddata + "," + str(tempdata)
        # convert the UNIX time to UTC and create the final string to append to the
        # returned array
        utc_time_now = unix_to_utc(time_now)
        finaldata = str(utc_time_now) + aggregateddata
        finaloutput.append(finaldata)

    # create the column headers and prepend to the return array
    headerstring = "Date/Time UTC"
    datathing = ""
    for item in stationlist:
        datathing = datathing + "," + item.name
    headerstring = headerstring + datathing

    finaloutput.reverse()
    finaloutput.append(headerstring)
    finaloutput.reverse()

    # append final aggregated data to output
    return finaloutput


# ##################################################
# Save out CSV data
# ##################################################
def save_csv(arraydata, savefile):
    try:
        os.remove(savefile)
    except:
        print("Error deleting old file")

    for line in arraydata:
        try:
            with open(savefile, 'a') as f:
                f.write(line + "\n")

        except IOError:
            print("WARNING: There was a problem accessing heatmap file")


# ##################################################
# Convert timestamps in array to UTC time
# ##################################################
def unix_to_utc(unixdate):
    utctime = datetime.datetime.fromtimestamp(int(unixdate)).strftime('%Y-%m-%d %H:%M:%S')
    return utctime


# ############################################
# Main method starrts here
# ############################################
if __name__ == "__main__":
    while True:
        # calculate the processing time
        sleeptime = 5 * 60  # delay the next iteration
        starttime = datetime.datetime.now()
        starttime = time.mktime(starttime.timetuple())

        # for each station.....
        for mag_station in station_list:
            mag_station.process_mag_station()

        # Create aggregate list of dF/dt
        # create the combined output file
        # convert the timesampts to UTC for display on the website
        aggregated_data = []
        aggregated_data = create_aggregated_magnetometer_values(station_list)

        # save to CSV or JSON OUTPUT file
        save_csv(aggregated_data, "aggregate.csv")

        # Calculate the elapsed processing time and display the result to the console...
        finishtime = datetime.datetime.now()
        finishtime = time.mktime(finishtime.timetuple())
        elapsedtime = finishtime - starttime

        # elapsedtime = float(elapsedtime / 60)
        print("\nCOMPLETED. Time to process data was " + str(elapsedtime) + " seconds")

        for i in range(0, sleeptime):
            print(str(sleeptime - i) + " seconds until next pass")
            time.sleep(1)
