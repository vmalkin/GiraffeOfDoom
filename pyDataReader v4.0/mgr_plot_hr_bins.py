from datetime import datetime
from statistics import mean, median

# assume the devices records data every 1 seconds. we want a running average of one minute
# half_window = 30


def filter_median(datavalues):
    templist = []

    for i in range(3, len(datavalues)):
        t = []
        dt = datavalues[i][0]
        t.append(float(datavalues[i][1]))
        t.append(float(datavalues[i-1][1]))
        t.append(float(datavalues[i-2][1]))

        if sum(t) > 0:
            medianvalue = median(t)
        else:
            medianvalue = 0

        dp = [dt ,str(medianvalue)]

        templist.append(dp)
    return templist


def filter_average_binner(datavalues):
    _binlength = 60
    returnlist = []
    bin = []
    for i in range(0, len(datavalues)):
        if i % _binlength == 0:
            if len(bin) > 2:
                binvalue = mean(bin)
            else:
                binvalue = 0

            datetime = datavalues[i][0]
            dp = [datetime, str(binvalue)]
            returnlist.append(dp)
            bin = []
        else:
            value = float(datavalues[i][1])
            bin.append(value)

    return returnlist


# def save_file(current_data, publishfolder):
#     savefile = publishfolder + "//dna_telluric.csv"
#     with open(savefile, "w") as s:
#         s.write("UTC Datetime, Smoothed Ambient Voltage" + "\n")
#         for item in current_data:
#             dt = int(float(item[0]))
#             # print(dt)
#             dt = posix2utc(dt)
#             data = item[1]
#             dp = dt + "," + str(data) + "\n"
#             s.write(dp)
#         s.close()


def posix2utc(posixtime):
    timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def wrapper(datavalues):
    templist = datavalues
    templist = filter_median(templist)
    templist = filter_average_binner(templist)
    return templist