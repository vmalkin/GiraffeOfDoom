import os
import matplotlib.pyplot as plt
import matplotsave as pltsave
from decimal import Decimal, getcontext

# Raw Data Format:
# Date/Time (UTC), Raw X, Raw Y, Raw Z
# 2016-10-10 00:00:26.19,-391.23,3349.61,1354.43

# for each file in list
# We might need some method to parse a datafile to see that the data 
# is valid, not noisy, has no blips, etc.




# ##################################################
# Prune Data - we only need Raw X value.
# ##################################################
def prune_data(arraydata):
    outputarray = []
    # we want to avoid the first line that contains a header text
    for i in range(1,len(arraydata)):
        dataline = arraydata[i].split(",")
        # dataline = re.split(r'[\s,]', item)
        newdata = dataline[1]
        outputarray.append(newdata)
    # print("Array is " + str(len(arraydata)) + " records long")
    return outputarray

# ##################################################
# Diffs Data - convert X values to differences.
# ##################################################
def diffs_data(arraydata):
    getcontext().prec = 5
    outputarray = []

    # Parse thru the input array
    for i in range(1, len(arraydata)):
        # grab the reading for now and the last reading
        nowdata = Decimal(arraydata[i])
        olddata = Decimal(arraydata[i - 1])

        # calculate the differences
        diff = Decimal(nowdata - olddata)

        # create the string to be appended
        outputline = str(diff)

        outputarray.append(outputline)

    # return array of differences
    # print("Array is " + str(len(arraydata)) + " records long")
    return outputarray


# ##################################################
# Running Average - smooth diffs
# ##################################################
def running_avg(arraydata):
    getcontext().prec = 5
    outputarray = []

    magrate = 4  # How many readings per minute from the magnetometer

    # for 10 min interval
    interval = 10

    #calculate thje running avg window size
    window = interval * magrate
    half_window = int(window / 2)

    for i in range(half_window, (len(arraydata) - half_window)):
        avgdiff = 0

        # calculate the avg either side of this time interval
        for j in range(0, window):
            avgdiff = avgdiff + Decimal(arraydata[i - half_window + j])

        avgdiff = Decimal(avgdiff / window)

        # create the data string to be written to list
        datastring = str(avgdiff)

        outputarray.append(datastring)

    # print("Array is " + str(len(arraydata)) + " records long")
    return outputarray


# ##################################################
# Daily Activity - create activity readings for the day
# ###################################################
def daily_readings(arraydata):
    getcontext().prec = 5
    maxvalue = 0
    minvalue = 0

    for item in arraydata:
        item = Decimal(item)
        if item >= minvalue and item <= maxvalue:
            pass # everything is ok

        if item >= maxvalue and item >= minvalue:
            maxvalue = item # this reading is largest

        if item <= maxvalue and item <=  minvalue:
            minvalue = item # this reading is smallest

    diff = maxvalue - minvalue

    return str(diff)

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
# Normalise data
# ##################################################
def normalise(arraydata):
    getcontext().prec = 5

    datamin = Decimal(1000)

    # first find the smallest value...
    for item in arraydata:
        item = item.split(",")
        item = item[1]
        if Decimal(item) <= Decimal(datamin):
            datamin = item

    # now find the largets value...
    datamax = Decimal(datamin)
    for item in arraydata:
        item = item.split(",")
        item = item[1]
        if Decimal(item) > Decimal(datamax):
            datamax = item

    temp_array = []

    print("max/min values: " + str(datamax) + "/" + str(datamin))

    diffvalue = Decimal(datamax) - Decimal(datamin)
    for i in range(0, len(arraydata)):
        item = arraydata[i].split(",")
        datetime = item[0]
        item = item[1]
        datavalue = (Decimal(item) - Decimal(datamin)) / Decimal(diffvalue)
        newdatastring = datetime + "," +str(datavalue)
        temp_array.append(newdatastring)

    return temp_array

# ##################################################
# Process a single CSV file
# ##################################################
def datarun(rawdatafile):
    print("Processing " + rawdatafile)
    # Load in CSV data
    rawdataarray = []
    if os.path.isfile(rawdatafile):
        try:
            with open(rawdatafile) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    rawdataarray.append(line)

        except IOError:
            print("File appears to be present, but cannot be accessed at this time. ")

    # Prune down rawdataarray to datetime and X values
    rawdataarray = prune_data(rawdataarray)


    # Convert list of absolute values into dH/dt
    rawdataarray = diffs_data(rawdataarray)

    # Smooth the array down
    rawdataarray = running_avg(rawdataarray)
    rawdataarray = running_avg(rawdataarray)

    # create the daily  readings
    reading = daily_readings(rawdataarray)

    return reading


# ##################################################
# M A I N   C O D E   S T A R T S  H E R E
# ##################################################
CSVlist = "files.txt"
CSVFilenames = []
finaldataarray = []

if os.path.isfile(CSVlist):
    try:
        with open(CSVlist) as e:
            for line in e:
                line = line.strip()  # remove any trailing whitespace chars like CR and NL
                CSVFilenames.append(line)

    except IOError:
        print("File appears to be present, but cannot be accessed at this time. ")

for items in CSVFilenames:
    reading = datarun(items)
    datalist = items.split(".")
    filename = datalist[0]
    finaldata = filename + "," + reading
    finaldataarray.append(finaldata)

# If necessary, normalise the data
# finaldataarray = normalise(finaldataarray)

save_csv(finaldataarray,"heatmap.csv")

# Create the heatmap plot of the data.
labelslist = []
datalist = []

for item in finaldataarray:
    data = item.split(",")
    labelslist.append(data[0])
    datavalue = Decimal(data[1])
    datalist.append(datavalue)

print(datalist)

plt.bar(range(len(datalist)), datalist, align='center')
plt.ylabel("dH/dt relative")
plt.xlabel("Date")
plt.title("Geomagnetic activity from " + labelslist[0] + " to " + labelslist[len(labelslist) - 1] + "\n")
plt.xticks(range(len(datalist)), labelslist, size='small', rotation='vertical')
plt.show()