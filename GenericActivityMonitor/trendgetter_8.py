import os
import time
from datetime import datetime
from time import mktime
import re
import math

BIN_SIZE = 60 * 10 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total
DURATION = 60*60*24
STORM_THRESHOLD = 14
aurora_sightings_list = "sightings.csv"

# ##################################################
# Datapoint class to be used.
# ##################################################
class DPbasic():
    def __init__(self, posixdate, data):
        self.posixdate = posixdate
        self.data = data

# ##################################################
# Datapoint class to be used.
# ##################################################
class DPbin():
    def __init__(self, posixdate):
        self.posixdate = posixdate
        self.datalist = []

    def datavalue(self):
        avgvalue = 0
        if len(self.datalist) > 0:
            for item in self.datalist:
                avgvalue = float(avgvalue) + float(item)

            avgvalue = avgvalue / float(len(self.datalist))
            avgvalue = round(avgvalue, 2)
        else:
            avgvalue = 0
        return avgvalue

    def print_values(self):
        returnstring = str(self.posixdate) + "," + str(self.datavalue())
        return returnstring


class Station():
    def __init__(self, stationname, datasource):
        self.station_name = stationname
        self.rawdata = []
        self.datasource = datasource

    def get_data(self):
        rawdatalist = []
        firstline = True
        with open(self.datasource) as e:
            print("Processing " + self.datasource)
            # Skip the first line in each file as it's a header
            for line in e:
                if firstline is True:
                    # print("Header identified, skipping...")
                    firstline = False
                else:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    rawdatalist.append(line)

        return rawdatalist

    def initial_list_parse(self, rawdatalist):
        # Out data should be in the format of timestamp, data1, data2, etc We only need the timestamp and the
        # first data value
        # convert the list into an array of datapoint objects, with posix timestamps
        print("Begin converting logfile data to [posixdate, data] format")
        regex = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d)'
        dateformat = "%Y-%m-%d %H:%M:%S.%f"
        initial_datalist = []
        errorcount = 0

        for item in rawdatalist:
            itemsplit = item.split(",")
            utcdate = itemsplit[0]
            datavalue = itemsplit[1]

            # if the date matches trhe regex format, attempt to convert to posix timestamp
            if re.match(regex, utcdate):
                newdatetime = datetime.strptime(utcdate, dateformat)
                # convert to Unix time (Seconds)
                newdatetime = mktime(newdatetime.timetuple())
                newdatetime = int(newdatetime)
                dp = str(newdatetime) + "," + str(datavalue)
                initial_datalist.append(dp)
            else:
                errorcount = errorcount + 1
        print(str(errorcount) + " errors in datetime encountered")
        return initial_datalist

    # ##################################################
    # convert a list to a list of objects.
    # ##################################################
    def convert_to_obj(list):
        returnlist = []
        for item in list:
            datasplit = item.split(",")
            date = datasplit[0]
            data = datasplit[1]
            dp = DPbasic(date, data)
            returnlist.append(dp)
        return returnlist

    # ##################################################
    # median filter this works on a CSV list [datetime, data]
    # ##################################################
    def medianfilter(self, datalist):
        returnlist = []
        for i in range(1, len(datalist) - 1):
            templist = []
            datasplit_v1 = datalist[i - 1].split(",")
            datasplit_v2 = datalist[i].split(",")
            datasplit_v3 = datalist[i + 1].split(",")

            v1 = datasplit_v1[1]
            v2 = datasplit_v2[1]
            datetime = datasplit_v2[0]
            v3 = datasplit_v3[1]

            templist.append(v1)
            templist.append(v2)
            templist.append(v3)
            templist.sort()

            datavalue = templist[1]
            dp = datetime + "," + datavalue

            returnlist.append(dp)
        return returnlist

    # ##################################################
    # Binning - this is essentially a hash function based
    # on the posix datetime
    # ##################################################
    def create_bins(objectlist):
        # we do NOT want decimal values for time, only ints
        date_now = int(time.time())

        # just while we work with the short dataset. Otherwise comment out
        # date_now = int(1528934391)

        date_start = date_now - DURATION

        binned_data = []
        for i in range(date_start, date_now, BIN_SIZE):
            dp = DPbin(i)
            binned_data.append(dp)

        # THis is the hashing function to drop data into the correct bins
        # according to the date.
        for i in range(0, len(objectlist)):
            bin_id = (float(objectlist[i].posixdate) - float(date_start)) / BIN_SIZE
            bin_id = int(round(bin_id, 0))
            binned_data[bin_id].datalist.append(objectlist[i].data)
        return binned_data

    def calc_dhdt(self, object_list):
        pass

    def calc_adjusted_dhdt(self, object_list):
        pass

    def save_json(self, object_list):
        pass

    def save_csv(self, object_list):
        pass

#
# # ##################################################
# # Write out values to file.
# # ##################################################
# def save_csv(arraydata, savefile):
#     try:
#         os.remove(savefile)
#     except:
#         print("Error deleting old file")
#
#     nope = DPPublish(0,0)
#     with open(savefile, 'a') as f:
#         f.write(nope.print_labels() + "\n")
#
#     for item in arraydata:
#         try:
#             with open(savefile, 'a') as f:
#                 f.write(item.print_values() + "\n")
#
#         except IOError:
#             print("WARNING: There was a problem accessing heatmap file")
#
#
# def initial_list_parse(rawdatalist):
#     # Out data should be in the format of timestamp, data1, data2, etc We only need the timestamp and the
#     # first data value
#     # convert the list into an array of datapoint objects, with posix timestamps
#     print("Begin converting logfile data to [posixdate, data] format")
#     regex = r'(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d)'
#     dateformat = "%Y-%m-%d %H:%M:%S.%f"
#     initial_datalist = []
#     errorcount = 0
#
#     for item in rawdatalist:
#         itemsplit = item.split(",")
#         utcdate = itemsplit[0]
#         datavalue = itemsplit[1]
#
#         # if the date matches trhe regex format, attempt to convert to posix timestamp
#         if re.match(regex, utcdate):
#             newdatetime = datetime.strptime(utcdate, dateformat)
#             # convert to Unix time (Seconds)
#             newdatetime = mktime(newdatetime.timetuple())
#             newdatetime = int(newdatetime)
#             dp = str(newdatetime) + "," + str(datavalue)
#             initial_datalist.append(dp)
#         else:
#             errorcount = errorcount + 1
#     print(str(errorcount) + " errors in datetime encountered")
#     return initial_datalist
#
#
# # ##################################################
# # median filter this works on a CSV list [datetime, data]
# # ##################################################
# def medianfilter(datalist):
#     returnlist = []
#     for i in range(1, len(datalist) - 1):
#         templist = []
#         datasplit_v1 = datalist[i - 1].split(",")
#         datasplit_v2 = datalist[i].split(",")
#         datasplit_v3 = datalist[i + 1].split(",")
#
#         v1 = datasplit_v1[1]
#         v2 = datasplit_v2[1]
#         datetime = datasplit_v2[0]
#         v3 = datasplit_v3[1]
#
#         templist.append(v1)
#         templist.append(v2)
#         templist.append(v3)
#         templist.sort()
#
#         datavalue = templist[1]
#         dp = datetime + "," + datavalue
#
#         returnlist.append(dp)
#     return returnlist
#
#
# # ##################################################
# # Convert the list to dh/dt
# # ##################################################
# def create_dhdt(object_list):
#     returnlist = []
#     dhdt_threshold = 5
#     for i in range(1, len(object_list)):
# #        prevsplit = filtered_datalist[i-1].split(",")
# #        nowsplit = filtered_datalist[i].split(",")
#
# #        prev_data = float(prevsplit[1])
# #        now_data = float(nowsplit[1])
# #        now_datetime = nowsplit[0]
#         prev_data = object_list[i-1].average_datalist()
#         now_data = object_list[i].average_datalist()
#         now_datetime = object_list[i].posixdate
#
#         dhdt = float(now_data) - float(prev_data)
#         if math.sqrt(math.pow(dhdt, 2)) > dhdt_threshold:
#             dhdt = 0
#
#         dp = DPPlain(now_datetime, dhdt)
#         returnlist.append(dp)
#     return returnlist
#
#
# # #################################################################################
# # Create the smoothed data array and write out the files for plotting.
# # We will do a running average based on the running average time in minutes and the number
# # readings per minute
# # Data format is a list of DP_Plain objects
# # #################################################################################
# def running_average(input_array, averaging_interval):
#     displayarray = []
#     if len(input_array) > averaging_interval:
#         for i in range(averaging_interval + 1, len(input_array)):
#             datavalue = 0
#             datetime = input_array[i].posixdate
#             for j in range(0, averaging_interval):
#                 newdata = input_array[i-j].data
#                 datavalue = float(datavalue) + float(newdata)
#
#             datavalue = round((datavalue / averaging_interval), 3)
#             appendvalue = DPPlain(datetime, datavalue)
#             displayarray.append(appendvalue)
#             # print("Smoothing: "+ str(i) + " / " + str(len(input_array)))
#     return displayarray
#
#
#
#
#
# # ##################################################
# # convert a list to a list of objects.
# # ##################################################
# def convert_to_obj(list):
#     returnlist = []
#     for item in list:
#         datasplit = item.split(",")
#         date = datasplit[0]
#         data = datasplit[1]
#         dp = DPPlain(date, data)
#         returnlist.append(dp)
#     return returnlist
#
# # ##################################################
# # convert a list to a list of DPPublist objects.
# # ##################################################
# def create_presentation(dhdt_objects):
#     returnarray = []
#     for item in dhdt_objects:
#         dp = DPPublish(item.posixdate, item.data)
#         returnarray.append(dp)
#     return returnarray
#
#
# # ##################################################
# # convert a list to a list of DPPublist objects.
# # ##################################################
# def storm(Publish_objects):
#     storm_threshold = 2.5
#
#     for item in Publish_objects:
#         if item.data > storm_threshold:
#             item.storm_threshold = storm_threshold
#         if item.data < storm_threshold * -1:
#             item.storm_threshold = storm_threshold
#
#
# # ##################################################
# # convert a list to a list of DPPublist objects.
# # ##################################################
# def aurora_sightings(publish_objects):
#     sightings = []
#     with open("sightings.csv") as e:
#         for line in e:
#             line = line.strip()  # remove any trailing whitespace chars like CR and NL
#             sightings.append(line)
#
# def plot_carringtons(publish_objects):
#     # a carrington cycle is 27 days or 2,356,585.92 seconds!
#     cc = 2356586 / BIN_SIZE
#     cc = int(round(cc, 0))
#     for i in range(0, len(publish_objects), cc):
#         publish_objects[i].carrington_point = 0
#         print(i)
#
#
# # ##################################################
# # convert a list to a list of DPPublist objects.
# # ##################################################
# def adjusted_data(publish_list):
#     for i in range(1, len(publish_list)):
#         temp = []
#         temp.append(publish_list[i-1].data)
#         temp.append(publish_list[i].data)
#         temp.sort()
#         publish_list[i].adjusteddata = round((float(temp[1]) - float(temp[0])),2)
#     return publish_list

# ##################################################
#
# S C R I P T   B E G I N S   H E R E
#
# ##################################################
# using the list of files, open each logfile into the main array
if __name__ == "__main__":
    # calculate the processing time
    starttime = time.time()
    station1 = Station("Ruru Observatory", "2018-07-18.csv")

    station1.rawdata = station1.get_data()
    station1.rawdata = station1.initial_list_parse(station1.rawdata)
    station1.rawdata = station1.medianfilter(station1.rawdata)
    station1.rawdata = station1.convert_to_obj(station1.rawdata)
    station1.rawdata = station1.create_bins(station1.rawdata)

    # # save_csv(magnetometer_data, "tg_rawmagdata.csv")
    #
    # # Convert the data to dH/dt.
    # dhdt_objects = create_dhdt(magnetometer_data)
    #
    # # Smooth the dhdt data
    # window = 2
    # dhdt_objects = running_average(dhdt_objects, window)
    # dhdt_objects = running_average(dhdt_objects, window)
    #
    # # Create the final list for presentation
    # # uses DPPublish object
    # dhdt_objects = create_presentation(dhdt_objects)
    #
    # # Adjust the dhdt to be from zero upwards
    # dhdt_objects = adjusted_data(dhdt_objects)
    #
    # # Add the Storm Threshold, Aurora Sighting data, carrinton markers
    # storm(dhdt_objects)
    # plot_carringtons(dhdt_objects)
    #
    # # Save the data out as a CSV file for display in highcharts
    # save_csv(dhdt_objects, "aurora_activity.csv")

    finishtime = time.time()
    elapsed = str(round((finishtime - starttime), 1))
    print("\nFinished. Time to process: " + elapsed + " seconds")

