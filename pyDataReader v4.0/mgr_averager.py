from datetime import datetime
from statistics import mean

#assume the devices records data every 3 seconds. we want a running average of one minute
half_window = 10

def save_smoothed_data(current_data, publishfolder):
    savefile = publishfolder + "//dna_ambrf.csv"
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


def smooth_data(datavalues):
    temparray = []
    for i in range(half_window, len(datavalues) - half_window):
        scratch = []
        datetime = datavalues[i][0]
        for j in range(0 - half_window, half_window):
            dv = datavalues[i + j][1]
            scratch.append(dv)
        newdatavalue = mean(scratch)
        dp = [datetime, newdatavalue]
        temparray.append(dp)
    return  temparray


def convert_times(tempdata):
    return tempdata


def wrapper(datavalues, publishdir):
    tempdata = smooth_data(datavalues)
    processeddata = convert_times(tempdata)

    save_smoothed_data(processeddata, publishdir)

