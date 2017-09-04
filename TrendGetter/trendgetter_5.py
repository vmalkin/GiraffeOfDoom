import os
from datetime import datetime
from time import mktime


BIN_SIZE = 60 * 60 * 24  # the number of seconds wide a bin is
BIN_NUMBER = 365  # how many bins we want in total

# ##################################################
# Prune Data - we only need Raw X value.
# ##################################################
def prune_data(arraydata):
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

        # Convert the UNix timestamp, inot a UTC string
        utcdate = datetime.fromtimestamp(unixdate)

        # Create the dataline to be appended
        dataline = str(utcdate) + "," + datasplit[1]
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
        maxvalue = arraylist[0]
        minvalue = arraylist[0]
        for item in arraylist:
            if item >=maxvalue:
                maxvalue = item
            if item <= minvalue:
                minvalue = item

        returnvalue = float(maxvalue) - float(minvalue)

    return returnvalue


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
# S C R I P T   B E G I N S   H E R E
# ##################################################
# using the list of files, open each logfile into the main array
if __name__ == "__main__":
    CSVlist = "files.txt"
    CSVFilenames = []
    rawdatalist = []
    print("Loading list of logfiles...")
    # load in the list of CSV files to process
    if os.path.isfile(CSVlist):
        try:
            with open(CSVlist) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    CSVFilenames.append(line)

        except IOError:
            print("List of logfiles appears to be present, but cannot be accessed at this time. ")

    print("Adding logfile data...")
    # Parse thru the CSVfilelist, Append values to our raw data list
    for item in CSVFilenames:
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
            print("A logfile appears to be present, but cannot be accessed at this time. ")

    # Out data should be in the format of timestamp, data1, data2, etc We only need the timestamp and the
    # first data value

    print("Getting timestamps and data...")
    rawdatalist = prune_data(rawdatalist)

    print("Converting timestamps to UNIX time...")
    # convert the timestamps in the main array to POSIX format
    rawdatalist = utc_2_unix(rawdatalist)

    # superfluous step as the binning process will deal with this.
    # print("Ensure list is sorted by time...")
    # # Sort the main array by timestamp oldest to newest
    # rawdatalist = sorted(rawdatalist, key=lambda datastring: datastring[0])

    print("Create dates for data bins...")
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
    # the array for final data
    finaldataarray = []

    # for each bin interval in the list of bin timestamps
    for i in range(0, len(bindates)):
        # set up a holding list
        templist = []

        # parse thru the main array entries that fit in the interval are added to the holding list
        for item in rawdatalist:
            itemsplit = item.split(",")
            itemdate = itemsplit[0]
            itemdata = itemsplit[1]

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

    # convert the POSIX datetimes back to UTC.
    # print("Converting time to UTC...")
    finaldataarray = unix_to_utc(finaldataarray)

    # create the header and save the file as a CSV/JSON
    save_csv(finaldataarray, "binned_values.csv")
    print("FINISHED: Data saved to CSV file.")
