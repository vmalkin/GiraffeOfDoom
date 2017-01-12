import Station
import os
from decimal import Decimal, getcontext
import time

getcontext().prec = 5

while True:
    # create the magnetometer stations for this run
    try:
        corstorphine01 = Station.Station("Corstorphine 01", "Corstorphine01.1minbins.csv")
    except:
        print("Unable to create station")

    try:
        dalmore02 = Station.Station("Dalmore 02", "Dalmore_Rapid.1minbins.csv")
    except:
        print("Unable to create station")

    try:
        dalmore01 = Station.Station("Dalmore 01", "Dalmore01.1minbins.csv")
    except:
        print("Unable to create station")

    # init the array of stations and append
    stationlist = []
    try:
        stationlist.append(dalmore01)
    except:
        print("Unable to create station")

    try:
        stationlist.append(dalmore02)
    except:
        print("Unable to create station")

    try:
        stationlist.append(corstorphine01)
    except:
        print("Unable to create station")

    # create a list of unique timestamps based on all available times from all stations, for this run.
    # make a list of all dates, duplicates and all...
    temp_data = []
    for magstation in stationlist:
        for i in range(0, len(magstation.output_f)):
            datasplit = magstation.output_f[i].split(",")
            testdate = datasplit[0]
            temp_data.append(testdate)

    # sort the list A-Z-wise
    temp_data.sort()

    olddate = "2000-01-01 00:00"
    date_data = []
    # Go thru the temp data and write out unique datetimes only, to the final merged list.
    for dateitem in temp_data:
        while dateitem != olddate:
            # print(dateitem)
            date_data.append(dateitem)
            olddate = dateitem


    merged_data = []
    print("Calculated date range...")
    # Now, for each dateitem in date_data...
    for dateitem in date_data:
        #  Set up a datastring.
        datastring = ""
        # Go thru each magnetometer station in the station list.
        for magstation in stationlist:
            # go thru each mag stations output list, find matching date and append the value to datastring
            tempstring = datastring
            for info in magstation.output_f:
                info = info.split(",")
                if info[0] == dateitem:
                    datastring = datastring + info[1] + ","

            # we went thru the list of stations and there was no entry for this date/time
            # CUSTOMISE the N/A string according to your graphing software so that N/A is not plotted
            if tempstring == datastring:
                datastring = datastring + ","

        merged_data.append(dateitem + "," + datastring)

    # for item in merged_data:
    #     print(item)

    print("Identified data...")

    temp_data= []
    # remove final trailing comma
    for item in merged_data:
        item = item[:-1]
        temp_data.append(item)
    merged_data = temp_data


    # One final task - re-write the final merged data for values that do NOT have a zero in them.
    # temp_data = []
    # for i in range(0, len(merged_data)):
    #     writeflag = 1
    #     datasplit = merged_data[i].split(",")
    #     for dataitems in datasplit:
    #         if dataitems == str(0):
    #             writeflag = 0 # we cannot write this line...
    #     if writeflag == 1:
    #         temp_data.append(merged_data[i])
    # merged_data = temp_data


    # insert the headings as the first element of the merged_data[]
    merged_header = "Date/Time UTC, "
    for magstation in stationlist:
        merged_header = merged_header + magstation.station_name + ","

    merged_header = merged_header + "Averaged Reading"

    # We only want the most recent 1440 entries
    if len(merged_data) > 1440:
        chopvalue = len(merged_data) - 1440
        try:
            print("Merged array is " + str(len(merged_data)) + " records long: Trimming array")
            merged_data = merged_data[chopvalue:]
            print("Merged array is now " + str(len(merged_data)) + " records long\n")
        except:
            print("ERROR: Unable to trim array")
    # add to merged_data array
    merged_data.reverse()
    merged_data.append(merged_header)
    merged_data.reverse()

    # write out to logfile
    logfile = "merged1.csv"
    try:
    try:
        os.remove(logfile)
    except OSError:
        print("WARNING: could not delete " + logfile)

    for readings in merged_data:
        try:
            with open(logfile, 'a') as f:
                f.write(readings + '\n')
                # print("Data logged ok. Array Size: " + str(len(readings)))
        except IOError:
            print("WARNING: There was a problem accessing the current logfile: " + logfile)
    print("Data merge COMPLETED")

    time.sleep(600)
