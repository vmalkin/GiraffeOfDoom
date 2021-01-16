from datetime import datetime
from statistics import mean, median

# assume the devices records data every 1 seconds. we want a running average of one minute
# half_window = 30


def filter_median(datavalues):
    templist = []

    for i in range(2, len(datavalues)):
        dt = datavalues[i][0]
        t = [datavalues[i][1], datavalues[i-1][1], datavalues[i-2][1]]
        medianvalue = median(t)
        dp = dt + "," + str(medianvalue)
        templist.append(dp)
    return templist


def filter_average_binner(datavalues):
    _binlength = 60
    returnlist = []
    bin = []
    for i in range(0, len(datavalues)):
        if i % _binlength == 0:
            binvalue = mean(bin)
            datetime = posix2utc(datavalues[i][0])
            dp = datetime + "," + str(binvalue)
            returnlist.append(dp)
        else:
            value = datavalues[i][1]
            bin.append(value)

    return returnlist


def save_file(current_data, publishfolder):
    savefile = publishfolder + "//dna_telluric.csv"
    with open(savefile, "w") as s:
        s.write("UTC Datetime, Smoothed Ambient Voltage" + "\n")
        for item in current_data:
            dt = posix2utc(item[0])
            data = item[1]
            dp = str(dt) + "," + str(data) + "\n"
            s.write(dp)
        s.close()


def posix2utc(posixtime):
    timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def wrapper(datavalues, publishdir):
    templist = filter_median(datavalues)
    templist = filter_average_binner(templist)
    save_file(templist, publishdir)
