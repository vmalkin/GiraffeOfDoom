import sqlite3
import constants as k
import logging
import time
import datetime
import os
from statistics import mean, median, stdev
"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.WARNING
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)
db = dna_core.cursor()
timeformat = '%Y-%m-%d %H:%M:%S'

# Only specific station data makes sense as detrended readings.
stations = ["Ruru_Obs", "GOES_16", "Geomag_Bz"]
# stations = k.stations

finish_time = int(time.time())
start_time = finish_time - (60 * 60 * 24)
binsize = 60
number_bins = int((finish_time - start_time) / binsize) + 2
null_value = ""
half_window = 90

class Residual:
    def __init__(self, posixdatetime, datavalue, avgdatavalue, std_dev=0):
        self.posixdatetime = posixdatetime
        self.datavalue = datavalue
        self.avgdatavalue = avgdatavalue
        self.std_dev = float(std_dev)

    def calc_residual(self):
        returnvalue = (self.datavalue - self.avgdatavalue)
        if self.avgdatavalue == 0:
            returnvalue = null_value
        return returnvalue

    def posix2utc(self):
        # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        utctime = datetime.datetime.utcfromtimestamp(int(self.posixdatetime)).strftime(timeformat)
        return utctime

    def printheader(self):
        return "UTC, Value, +1SD, -1SD, +2SD, -2SD"

    def printdata(self):
        # returnstring = str(self.posix2utc()) +","+ str(self.calc_residual())
        returnstring = str(self.posix2utc()) + "," + str(self.calc_residual()) + "," + str(self.std_dev * 1) + "," + str(self.std_dev * -1) + "," + str(self.std_dev * 2) + "," + str(self.std_dev * -2)
        # returnstring = str(self.posix2utc()) + "," + str(self.datavalue)+ "," + str(self.avgdatavalue)+ "," + str(self.calc_residual())
        return returnstring

class DataPoint:
    def __init__(self, timevalue):
        self.datalist = []
        self.timevalue = timevalue

    def avg_data(self):
        if len(self.datalist) > 0:
            return float(mean(self.datalist))
        else:
            return null_value

    def max_data(self):
        if len(self.datalist) > 0:
            return float(max(self.datalist))
        else:
            return 0

    def min_data(self):
        if len(self.datalist) > 0:
            return float(min(self.datalist))
        else:
            return 0


def filter_median(list):
    """Takes in a list of DataPoints and performs a median filter on the object's datavalue"""
    filterwindow = 3
    returnlist = []
    for i in range(filterwindow, len(list)):
        medianstore = []
        datetime = list[i][0]
        for j in range(0, filterwindow):
            k = i - j
            datavalue = list[k][1]
            medianstore.append(datavalue)

        if len(medianstore) > 0:
            data = median(medianstore)
            dp = (datetime, data)
            returnlist.append(dp)
    return returnlist


def bin_indexvalue(nowtime):
    returnvalue = int((int(nowtime) - start_time) / binsize)
    return returnvalue


def check_create_folders():
    for station in stations:
        try:
            if not os.path.exists(station):
                print("Create directory for " + station)
                os.makedirs(station)
            else:
                print("Directory exists for " + station)
        except Exception:
            print("Some kind of error happened creating the directory for " + station)


def get_data(station):
    result = db.execute("select station_data.posix_time, station_data.data_value from station_data "
                        "where station_data.station_id = ? and station_data.posix_time > ?", [station, start_time])

    query_result = result.fetchall()
    return query_result


def parse_querydata(querydata):
    # turn the readings into rate of change.
    tempdata = []
    for i in range(1, len(querydata)):
        date = querydata[i][0]
        newdata = querydata[i][1]
        dp = (date, newdata)
        tempdata.append(dp)
    return tempdata


def save_logfiles(filename, datalist):
    d = Residual(0,0,0)
    with open(filename, "w") as n:
        n.write(d.printheader() + "\n")
        for item in datalist:
            n.write(item.printdata() + "\n")
    n.close()


def bin_data(tempdata):
    datapoint_list = []
    timestamp = start_time
    for i in range(0, number_bins):
        dp = DataPoint(timestamp)
        datapoint_list.append(dp)
        timestamp = timestamp + binsize

    for item in tempdata:
        try:
            index = bin_indexvalue(item[0])
            data = float(item[1])
            datapoint_list[index].datalist.append(data)
        except IndexError:
            print("Index error in datapoint list")

    binned_data = []
    # Calculate the difference between the min and max in the bin
    for item in datapoint_list:
        timevalue = item.timevalue

        if item.avg_data() == null_value:
            datavalue = 0
        else:
            datavalue = float(item.avg_data())

        datavalue = round(datavalue, 3)
        dp = (timevalue, datavalue)
        binned_data.append(dp)
    return binned_data


def calc_average_curve(datapoint_list):
    returnlist = []
    for item in datapoint_list:
        dp = Residual(item[0], item[1], 0, new_std_dev)
        returnlist.append(dp)

    for i in range(half_window, len(returnlist) - half_window):
        templist = []
        for j in range(-1 * half_window, half_window):
            d = float(returnlist[i + j].datavalue)
            templist.append(d)
        meanvalue = mean(templist)
        returnlist[i].avgdatavalue = meanvalue
    return returnlist


def calc_stddev(tempdata):
    datavalues = []
    for item in tempdata:
        datavalues.append(item[1])
    std_dev = round(stdev(datavalues),3)
    # print(std_dev)
    return std_dev


def writetoDB_std_dev(new_std_dev):
    db.execute("insert into station_statistics (station_id, std_dev) values (?, ?)", [station, new_std_dev])


def get_stdev_db_stdev():
    std_dev = 0
    result = db.execute("select std_dev from station_statistics where station_statistics.station_id = ?", [station])
    query_result = result.fetchall()

    if len(query_result) > 2:
        # invert the list, most recent at the top
        query_result.reverse()
        temp = []
        counter = 0
        for line in query_result:
            temp.append(line[0])
            counter += 1
            # we only want the first 1000 readings for this
            if counter == 1000:
                break
        std_dev = stdev(temp)
    return std_dev


if __name__ == "__main__":
    # check_create_folders()
    for station in stations:
        current_stationdata = get_data(station)

        tempdata = parse_querydata(current_stationdata)  # a list
        tempdata = filter_median(tempdata)  # a list
        tempdata = bin_data(tempdata)  # a list
        #


        # Update the latest standard deviation data
        new_std_dev = calc_stddev(tempdata)

        writetoDB_std_dev(new_std_dev)
        std_dev = get_stdev_db_stdev()

        # All other calculations are worked on data at 1 minute intervals,
        # incl calculation of K-index, etc.
        # create the 3 hour curve, and calculate the residuals
        residual_data = calc_average_curve(tempdata)

        nowfile = station + "_dxdt.csv"
        save_logfiles(nowfile, residual_data)

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
