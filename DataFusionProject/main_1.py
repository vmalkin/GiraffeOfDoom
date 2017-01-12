import Station_1
import os
from decimal import Decimal, getcontext
import time

getcontext().prec = 5

# Convert the times in the final data from Unix to UTC for display
def convertunixtoUTC(datalist):
    templist = []
    return templist

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


def current24hour(array):
    chopvalue = len(array) - 1440
    array = array[chopvalue:]
    return array

def createmerge(datelist, stationlist):
    # Next, we want to check each station in our station list. If it has a datavalue that falls in between the current
    # stamp, and the next one, we need to append it's data. If it does not, then we need to append a null reading.
    nulldatavalue = ""  # this may have to be "NULL", "0", etc, depending on our charting API
    mergeddataarray = []

    for i in range(0, len(datelist) - 1):
        d1 = datelist[i]
        d2 = datelist[i + 1]
        appenddata = ""
        for magstation in stationlist:
            for j in range(0, len(magstation.stationdata)):
                datasplit = magstation.stationdata[j].split(",")
                if float(datasplit[0]) >= float(d1) and float(datasplit[0]) < float(d2):
                    appenddata = datasplit[1] + ","

                else:
                    appenddata = nulldatavalue + ","

        appenddata = str(d1) + "," + appenddata
        mergeddataarray.append(appenddata)

    return mergeddataarray


# #########################################
# M a i n   p r o g r a m   h e r e
# #########################################
while True:
    # create the magnetometer stations for this run
    try:
        corstorphine01 = Station_1.Station("Corstorphine 01", "Corstorphine01.1minbins.csv")
    except:
        print("Unable to create station")

    try:
        dalmore02 = Station_1.Station("Dalmore 02", "Dalmore_Rapid.1minbins.csv")
    except:
        print("Unable to create station")

    try:
        dalmore01 = Station_1.Station("Dalmore 01", "Dalmore01.1minbins.csv")
    except:
        print("Unable to create station")

    # init the array of stations and append
    stations = []
    try:
        stations.append(dalmore01)
    except:
        print("Unable to create station")

    try:
        stations.append(dalmore02)
    except:
        print("Unable to create station")

    try:
        stations.append(corstorphine01)
    except:
        print("Unable to create station")

    # By this point station timestamps are in UNix time. Prime the earliest and latest time holders
    starttime = stations[0].begintime
    endtime = stations[0].endtime

    for i in range(1,len(stations)):
        if stations[i].begintime < starttime:
            starttime = stations[i].begintime

        if stations[i].endtime > endtime:
            endtime = stations[i].endtime

    # start end end times in UNIX format exist. We can calculate how many minutes this is and create a new array
    # that has prepopulated timeslot values based on this. Let us calculate this, and to be safe, add an extra minute
    # in case we have a remainder.
    totalmins = int((float(endtime) - float(starttime)) / 60)
    print("There are " + str(totalmins) + " total entries.")

    # Begin to build up the array. First create list of allowable time values.
    datevalues = []
    for i in range(int(float(starttime)), int(float(endtime)), 60):
        datevalues.append(i)

    # but we only weant the last 24 hours. so lets deal with that now
    datevalues = current24hour(datevalues)
    print("Array will be " + str(len(datevalues)) + " records long. Begin processing...")

    # create the merged data using the date and station lists
    mergeddataarray = createmerge(datevalues, stations)

    # Convert the times back to UTC.

    # save this array
    savedata(mergeddataarray)



    time.sleep(600)