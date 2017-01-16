import Station
import os
from decimal import Decimal, getcontext
import time
import datetime

getcontext().prec = 5

# ####################################################################################
# converts the UTC timestamp to unix time. returns converted array.
# ####################################################################################
def addheader(dataarray, stationlist):
    header = "date/time UTC"
    for magstation in stationlist:
        header = header + "," + magstation.station_name

    dataarray.reverse()
    dataarray.append(header)
    dataarray.reverse()

    return dataarray

# ####################################################################################
# converts the UTC timestamp to unix time. returns converted array.
# ####################################################################################
def unix2utc(dataarray):
    temparray = []
    for item in dataarray:
        data = item.split(",")
        unixdate = data[0]
        datavalue = ""

        for i in range(1, len(data)):
            datavalue = datavalue + "," + data[i]

        utctime = datetime.datetime.fromtimestamp(int(unixdate)).strftime('%Y-%m-%d %H:%M:%S')

        appenddata = str(utctime) + datavalue
        temparray.append(appenddata)
    return temparray

# ####################################################################################
# Saves array to display file
# ####################################################################################
def savedata(csvdata):
    # save data to CSV display file
    logfile = "merged.csv"
    try:
        os.remove(logfile)
    except OSError:
        print("WARNING: could not delete " + logfile)

    for readings in csvdata:
        try:
            with open(logfile, 'a') as f:
                f.write(readings + '\n')
                # print("Data logged ok. Array Size: " + str(len(readings)))
        except IOError:
            print("WARNING: There was a problem accessing the current logfile: " + logfile)

# ####################################################################################
# shrinks array to the last 24 hours only
# ####################################################################################
def current24hour(array):
    chopvalue = len(array) - 1440

    if len(array) > 1440:
        array = array[chopvalue:]

    return array

# ####################################################################################
# creates the final merged data
# ####################################################################################
def createmerge(datelist, stationlist):
    # Next, we want to check each station in our station list. If it has a datavalue that falls in between the current
    # stamp, and the next one, we need to append it's data. If it does not, then we need to append a null reading.
    nulldatavalue = ""  # this may have to be "NULL", "0", etc, depending on our charting API
    mergeddataarray = []

    for j in range(0, len(datelist) - 1):
        appenddata = ""
        d1 = datelist[j]
        d2 = datelist[j + 1]

        # for each station
        for j in range(0, len(stationlist)):
            tempdata = ","
            for i in range(0, len(stationlist[j].stationdata)):
                datasplit = stationlist[j].stationdata[i].split(",")
                if datasplit[0] >= str(d1) and datasplit[0] < str(d2):
                    tempdata = "," + datasplit[1]

            appenddata = appenddata + tempdata

        appenddata = str(d1) + appenddata
        # print(appenddata)
        mergeddataarray.append(appenddata)



    return mergeddataarray


# #########################################
# M a i n   p r o g r a m   h e r e
# #########################################
while True:
    # create the magnetometer stations for this run

    Dalmore1 = Station.Station("Dalmore01", "Dalmore01.1minbins.csv")


    time.sleep(600)