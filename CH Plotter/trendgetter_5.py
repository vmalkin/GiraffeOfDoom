import os
import logging
from datetime import datetime
from time import mktime
from decimal import Decimal, getcontext

__version__ = "2.0"
__author__ = "Vaughn Malkin"

BIN_SIZE = 60 * 60 # the number of seconds wide a bin is
BIN_NUMBER = int(31536000 / BIN_SIZE)  # how many bins we want in total
BINNED_PRELIM_DATA = "binned_preliminary_data.csv"
BINNED_FINAL_DATA = "aurora_activity.csv"
PREDICTION = "aurora_prediction.csv"
AURORA_SIGHTINGS = "aurorasitings.csv"
STORM_THRESHOLD = 6  # The threshold value for when we have a storm
AURORA_REPORTED = STORM_THRESHOLD * 1.2
NULLVALUE = "0"  # the null value for charting software

# logging levels in order of severity:
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL

errorloglevel = logging.WARNING
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
#
# we will divide this number evenly so our average represents the midpoint of these
# readings.
# #################################################################################
def running_average(input_array):
    getcontext().prec = 6
    displayarray = []

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = 6
    AVERAGING_TIME_HALF = int(AVERAGING_TIME / 2)

    # NOW average the cumulative array, smooth out the blips
    if len(input_array) > AVERAGING_TIME:
        for i in range(AVERAGING_TIME_HALF, len(input_array) - AVERAGING_TIME_HALF):
            xvalue = Decimal(0)
            jdatasplit = input_array[i].split(",")
            jdatadate = jdatasplit[0]

            # This is where we average for the time i before and after i.
            for j in range(0, AVERAGING_TIME):
                datasplit = input_array[(i - AVERAGING_TIME_HALF) + j]
                datasplit = datasplit.split(",")
                xdata = datasplit[1]

                xvalue = xvalue + Decimal(xdata)

            xvalue = Decimal(xvalue / AVERAGING_TIME)

            displaypoint = jdatadate + "," + str(xvalue)
            displayarray.append(displaypoint)

    else:
        displayarray = input_array

    return displayarray


# ##################################################
# Prune Data - we only need Raw X value.
# ##################################################
def prune_data(arraydata):
    logging.debug("shorten each data line to datetime and x value")
    outputarray = []
    # we want to avoid the first line that contains a header text
    for i in range(0,len(arraydata)):
        try:
            dataline = arraydata[i].split(",")
            # print(dataline)
            datetime = dataline[0]
            datavalue = dataline[1]
            newdata = datetime + "," + datavalue
            # print("Pruning " + str(i) + " of " + str(len(arraydata)) + " records.")
            outputarray.append(newdata)
        except:
            logging.debug("There is a problem with this data value - isolate the log file it belongs to and check: ")
            logging.debug("--> " + str(arraydata[i-1]))
            logging.debug("--> " + str(arraydata[i]))
            logging.debug("--> " + str(arraydata[i + 1]))

            print("There is a problem with this data value - isolate the log file it belongs to and check: ")
            print("--> " + str(arraydata[i-1]))
            print("--> " + str(arraydata[i]))
            print("--> " + str(arraydata[i + 1]))

    return outputarray

# ##################################################
# Convert timestamps in array to Unix time
# ##################################################
def utc_2_unix(arraylist):
    print("Converting time to UNIX time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d %H:%M:%S.%f"
    workingarray = []

    # convert array data times to unix time
    workingarray = []
    for item in arraylist:
        try:
            datasplit = item.split(",")

            newdatetime = datetime.strptime(datasplit[0],dateformat)
            # convert to Unix time (Seconds)
            newdatetime = mktime(newdatetime.timetuple())

            datastring = str(newdatetime) + "," + datasplit[1]
            workingarray.append(datastring)
        except:
            logging.debug("UTC 2 Unix: Problem with this entry: " + item)
            print("Problem with this entry: " + item)

    return workingarray

# ##################################################
# Convert timestamps in array to UTC time
# ##################################################
def unix_to_utc(arraylist):
    print("Converting time to UTC time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d %H:%M:%S.%f"

    # Convert the date string to the format of: 2016-10-10 00:00:26.19
    returnarray = []

    for item in arraylist:
        datasplit = item.split(",")
        unixdate = int(float(datasplit[0]))

        # remove the date part of the split
        datasplit.pop(0)

        # Convert the UNix timestamp, inot a UTC string
        utcdate = datetime.fromtimestamp(unixdate)

        # Create the dataline to be appended. Iterate thru the rest of the datasplit
        # and append it to the converted datetime
        dataline = ""
        for thing in datasplit:
            dataline = dataline + "," + str(thing)

        dataline = str(utcdate) + dataline
        returnarray.append(dataline)

    return returnarray

# ##################################################
# Find the average of an array of values
# ##################################################
def array_average(arraylist):
    returnvalue = 0
    if len(arraylist) == 0:
        returnvalue = 0
    else:
        for item in arraylist:
            returnvalue = float(returnvalue) + float(item)

        returnvalue = float(returnvalue) / float(len(arraylist))

    return returnvalue

# ##################################################
# Find the diff between max and min values of an array of values
# ##################################################
def array_diffs(arraylist):
    returnvalue = 0
    if len(arraylist) == 0:
        returnvalue = 0
    else:
        maxvalue = float(arraylist[0])
        minvalue = float(arraylist[0])
        for i in range(0, len(arraylist)):
            if float(arraylist[i]) >= float(maxvalue):
                maxvalue = arraylist[i]
            if float(arraylist[i]) <= float(minvalue):
                minvalue = arraylist[i]

        returnvalue = float(maxvalue) - float(minvalue)

    return returnvalue

# ##################################################
# median filter
# ##################################################
def medianfilter(arraylist):
    filteredlist = []
    for i in range(1,len(arraylist) - 1):
        templist = []
        templist.append(arraylist[i-1])
        templist.append(arraylist[i])
        templist.append(arraylist[i + 1])

        sortedlist = sorted(templist, key=lambda datastring: datastring[0])

        filteredlist.append(sortedlist[1])
    return filteredlist

# ##################################################
# load CSV data
# ##################################################
def load_csv(savefile):
    returnarray = []
    try:
        with open(savefile, 'r') as f:
            for line in f:
                line = line.strip()  # remove any trailing whitespace chars like CR and NL
                returnarray.append(line)
    except IOError:
        print("WARNING: There was a problem accessing heatmap file")
    return returnarray

# ##################################################
# Write out values to file.
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
# Append marker for geomagnetic Storm
# ##################################################
def geomagnetic_storm(arraydata):
    returnarray = []
    placeholder = []  # the data to be appended to the data

    # Loop thru the arraydata
    # for each line, test the data portion
    for item in arraydata:
        itemsplit = item.split(",")
        datavalue = itemsplit[1]

        # if the value =< threshold, append the threshold value to placeholder array, else append nullvalue
        if float(datavalue) >= float(STORM_THRESHOLD):
            placeholder.append(STORM_THRESHOLD)
        else:
            placeholder.append(NULLVALUE)

    # Then, for each item in the arraydata, concatenate the corresponding index from the placeholder.
    for i in range(0, len(arraydata)):
        returnvalue = ""
        # datasplit = arraydata[i].split(",")
        # returndate = datasplit[0]
        # returndata = datasplit[1]
        returndata = arraydata[i]
        returnthreshold = placeholder[i]

        # returnvalue = str(returndate) + "," + str(returndata) + "," + str(returnthreshold)
        returnvalue = str(returndata) + "," + str(returnthreshold)

        returnarray.append(returnvalue)

    return returnarray

# ##################################################
# Append marker for Aurora Sighting
# ##################################################
def aurora_sighting(arraydata):
    print("Appending Aurora Sighting Data")
    # load csv file of aurora sightng dates
    sightingdata = load_csv(AURORA_SIGHTINGS)
    placeholder = []  # The data that will be appended to each entry in the CSV
    returndata = []

    # Convert dates to Unix time
    logging.debug("Converting aurora sighting to UNIX time")
    sightingdata = utc_2_unix(sightingdata)

    # The UTC converter normally expects to append data after the time, so we have a comma after the date. Lets prune this
    templist = []
    logging.debug("Purging extra comma from converted sighting list")
    for item in sightingdata:
        itemsplit = item.split(",")
        unixdate = itemsplit[0]

        templist.append(str(unixdate))
    sightingdata = templist

    logging.debug("Creating placeholder list for aurora sightings")
    # parse thru array data if a date matches append the placeholder value, otherwise, append a zero
    for item in arraydata:
        itemsplit = item.split(",")
        itemdate = itemsplit[0]

        sightedmatches = NULLVALUE
        for jtem in sightingdata:
                if itemdate == jtem:
                    sightedmatches = AURORA_REPORTED

        placeholder.append(sightedmatches)

    # The placeholder array should be populated. Append its values to arraydata
    for i in range(0, len(arraydata)):
        returnitem = arraydata[i] + "," + placeholder[i]
        returndata.append(returnitem)

    return returndata

# ##################################################
# process conronal hole predictions
# ##################################################
def prediction(arraydata):
    pass

# ##################################################
# S C R I P T   B E G I N S   H E R E
# ##################################################
# using the list of files, open each logfile into the main array
if __name__ == "__main__":

    finaldataarray = []  # the array for final data

    # calculate the processing time
    starttime = datetime.now()
    starttime = mktime(starttime.timetuple())

    if not os.path.isfile(BINNED_PRELIM_DATA):
        logging.debug("preliminary binned data file does not exist, creating")

        CSVlist = "files.txt"
        CSVFilenames = []
        rawdatalist = []
        print("Loading list of logfiles...")
        # load in the list of CSV files to process
        logging.debug("Load in list of CSV data file names.")
        if os.path.isfile(CSVlist):
            try:
                with open(CSVlist) as e:
                    for line in e:
                        line = line.strip()  # remove any trailing whitespace chars like CR and NL
                        CSVFilenames.append(line)

            except IOError:
                logging.debug("List of logfiles appears to be present, but cannot be accessed at this time.")
                print("List of logfiles appears to be present, but cannot be accessed at this time. ")

        print("Adding logfile data...")
        # Parse thru the CSVfilelist, Append values to our raw data list
        for item in CSVFilenames:
            logging.debug("Begin parse of CSV data.")
            firstline = True
            try:
                with open(item) as e:
                    print("Processing " + item)
                    # Skip the first line in each file as it's a header
                    for line in e:
                        if firstline == True:
                            # print("Header identified, skipping...")
                            firstline = False
                        else:
                            line = line.strip()  # remove any trailing whitespace chars like CR and NL
                            rawdatalist.append(line)

            except IOError:
                logging.debug("A logfile appears to be present, but cannot be accessed at this time. ")
                print("A logfile appears to be present, but cannot be accessed at this time. ")

        # Out data should be in the format of timestamp, data1, data2, etc We only need the timestamp and the
        # first data value
        print("Getting timestamps and data...")

        rawdatalist = prune_data(rawdatalist)

        print("Converting timestamps to UNIX time...")
        # convert the timestamps in the main array to POSIX format
        rawdatalist = utc_2_unix(rawdatalist)

        print("Applying median filter for blips...")
        rawdatalist = medianfilter(rawdatalist)

        print("Create dates for data bins...")
        logging.debug("Create dates for data bins...")
        # using the most recent date in the main array, create  temp list of bin dates
        # THis will need to take into account the number and size of bins that we want.
        datasplit = rawdatalist[len(rawdatalist) - 1]
        datasplit = datasplit.split(",")
        nowdate = datasplit[0]

        bindates = []
        for i in range(0, BIN_NUMBER):
            bindates.append(nowdate)
            nowdate = float(nowdate) - float(BIN_SIZE)

        # this list is back to front, so reverse it - item[0] is older than item[10]
        bindates.reverse()

        print("Preparing array for final data")
        logging.debug("Preparing array for final data")
        # for each bin interval in the list of bin timestamps
        for i in range(0, len(bindates)):
            # set up a holding list
            templist = []

            # parse thru the main array entries that fit in the interval are added to the holding list
            for j in range(0, len(rawdatalist)):
                itemsplit = rawdatalist[j].split(",")
                itemdate = itemsplit[0]
                itemdata = itemsplit[1]
                # print(itemdate)

                if float(itemdate) <= float(bindates[i]) and float(itemdate) > float(bindates[i-1]):
                    templist.append(itemdata)

                # PERFORM WHATEVER OPERATION WE WANT, AVERAGE OR DH/DT, ETC
                # we now have a list templist[] of values for this bin
                # print("Averaging bin contents: " + str(i) + " / " + str(len(bindates)) + "...")
                # binvalue = array_average(templist)

            print("Calculating dH/dt for bins: " + str(i) + " / " + str(len(bindates)) + "...")
            binvalue = array_diffs(templist)

            finaldataitem = str(bindates[i]) + "," + str(binvalue)
            finaldataarray.append(finaldataitem)

        # AT this point we have list of entries, the format of each is
        # datestamp_posix_format, dh_dt_bin_value.
        # SAVE this list at this point. This has been the most time consuming operation so far, and if we dont need to
        # redo it then good.
        save_csv(finaldataarray, BINNED_PRELIM_DATA)
    else:
        logging.debug("Using existing calculated binned data values")
        print("Using existing caluclated binned data values")
        finaldataarray = load_csv("binned_preliminary_data.csv")

    # SMooth the data
    finaldataarray = running_average(finaldataarray)
    finaldataarray = running_average(finaldataarray)

    # calculate if any readings go over geomagnetic storm threshold. Append the value to correct date bins if they do
    finaldataarray = geomagnetic_storm(finaldataarray)

    # Match any dates with recorded aurora sightings. Append the value to correct date bins if they do
    finaldataarray = aurora_sighting(finaldataarray)

    # DATA ARRAY now has the format posix_date, dh/dt, storm_detect, aurora_reported
    # Run prediction
    print("Running Coronal Hole Prediction")
    prediction(finaldataarray)

    # convert the POSIX datetimes back to UTC.
    # print("Converting time to UTC...")
    finaldataarray = unix_to_utc(finaldataarray)

    # save the file as a CSV
    save_csv(finaldataarray, BINNED_FINAL_DATA)
    print("FINISHED: Data saved to CSV file.")
    finishtime = datetime.now()
    finishtime = mktime(finishtime.timetuple())

    elapsedtime = finishtime - starttime
    elapsedtime = float(elapsedtime / 60)
    print("\nElapsed time is " +str(elapsedtime) + " minutes.")
