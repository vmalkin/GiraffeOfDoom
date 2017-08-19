import Station
import logging
import datetime
import time

# #################################################################################
# Adjust these parameters according to the datadata...
# #################################################################################
# this is the size datatime between magnetometer readings. MUST be the same for all stations being used.
data_bin_size = 60
combined_listlength = int(86400 / data_bin_size)
# this is the delay for the while loop for updating the csv files...
sleeptime = 120

# ####################################################################################
# converts the UTC timestamp to unix datatime. returns converted array.
# ####################################################################################
def unix2utc(unixdate):
    utctime = datetime.datetime.fromtimestamp(int(unixdate)).strftime('%Y-%m-%d %H:%M:%S')
    return utctime

# #################################################################################
# Save the binned datadata as CSV file
# #################################################################################
def SaveAsCSV(datalist):
    # export array to array-save file
    try:
        with open("/home/vmalkin/Magnetometer/publish/combo.csv", 'w') as w:
            for item in datalist:
                w.write(item + '\n')
    except IOError:
        print("WARNING: There was a problem saving binned CSV datadata")

if __name__ == "__main__":
    # Setup error/bug logging
    # logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=logging.ERROR)
    logging.info("Created error log for this session")

    # create the entries for each station
    logging.info("Creating the instance of each station...")

    while True:
        # station1 = Station.Station("Dalmore Rapid No 1", "dr_01hr.csv")
        station1 = Station.Station("Dalmore Prime", "/home/vmalkin/Magnetometer/publish/Dalmore_Prime.1minbins.csv")

        # station2 = Station.Station("Dalmore Rapid No 2", "dr_02hr.csv")
        station2 = Station.Station("Dalmore Rapid No 1", "/home/vmalkin/Magnetometer/dalmoreR1/pyDataReader/graphing/Dalmore_Rapid_01.1minbins.csv")
        station3 = Station.Station("Dalmore Rapid No 2", "/home/vmalkin/Magnetometer/dalmoreR2/pyDataReader/graphing/Dalmore_Rapid_02.1minbins.csv")
        station4 = Station.Station("Corstorpine", "/home/vmcdonal/vicbins/Corstorphine01.1minbins.csv")

        # we're only ever going to have a handful of stations here, so just manually append them
        logging.info("Creating the list of magnetometer stations")
        stationlist = [station1, station2, station3, station4]

        # ##############################################################################################################
        # create the combined list. We will create a series of bins. The datetime range will be from the earliest to the
        # latest timestamp found from all the station datasets
        # find the earliest and latest datatime values from all the stations datadata

        time_start = 2000000000
        time_end = -2000000000

        for station in stationlist:
            datasplit = station.station_data[0].split(",")
            if float(datasplit[0]) < float(time_start):
                time_start = datasplit[0]

        for station in stationlist:
            finalindex = len(station.station_data) - 1
            datasplit = station.station_data[finalindex].split(",")
            if float(datasplit[0]) > float(time_end):
                time_end = datasplit[0]

        buckets = (float(time_end) - float(time_start)) / float(data_bin_size)
        logging.info("Start datatime is: " + str(time_start) + " End datatime is: " + str(time_end) + " " + str(buckets) + " records stored")

        # now start building up the final array of combined datadata. Begin by setting up the timestamps
        time_start = time_start.split(".")
        time_start = int(time_start[0])
        time_end = time_end.split(".")
        time_end = int(time_end[0])

        timestamps = []
        for i in range(time_start, time_end, data_bin_size):
            timestamps.append(i)

        # now using the defined timestamps, go thru each station datadata and place it's reading in the correct spot
        # if a station has no datadata for that timestamp then it's a null.
        NULLVALUE = "#n/a"
        combineddata = []

        # for each timestamp that we have...
        for i in range(1, len(timestamps)):
            appenddata = ""
            # ...we check each station in our list...
            for station in stationlist:
                data_found = False
                for item in station.station_data:
                    # ...we check the datadata of each station...
                    itemsplit = item.split(",")
                    datatime = itemsplit[0]
                    datadata = itemsplit[1]
                    # ...and if a datapoint falls in the bounds of a timestamp, we append it
                    # to a string...
                    if datatime < str(timestamps[i]) and datatime >= str(timestamps[i-1]):
                        stationdataitem = datadata
                        data_found = True

                    if data_found == False:
                        stationdataitem = NULLVALUE

                appenddata = appenddata + "," + stationdataitem

            utctime = unix2utc(timestamps[i])
            finaldata = str(utctime) + appenddata
            combineddata.append(finaldata)

        # convert times back to UTC, prune to correct number of values, add a header to the final file.
        print("Length of combined list: " + str(len(combineddata)) + ". Should be " + str(combined_listlength))
        if len(combineddata) > combined_listlength:
            slice_start = len(combineddata) - combined_listlength
            combineddata = combineddata[slice_start:]

        print("Length of final list: " + str(len(combineddata)))

        combineddata.reverse()
        heading = "Date/Time UTC"
        for station in stationlist:
            heading = heading + "," + station.station_name
        combineddata.append(heading)
        combineddata.reverse()

        SaveAsCSV(combineddata)

        print("FINISHED processing. Data saved to display file.\n")

        time_to_sleep = sleeptime
        for i in range(time_to_sleep, 0, -1):
            print(str(i) + " seconds until next run...")
            time.sleep(1)