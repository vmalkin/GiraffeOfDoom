"""
This is the instrument manager for Dunedin Aurora.

logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
from instruments import Datapoint
from instruments import MagGOES_16

from time import sleep, time
import datetime
import constants as k
import logging
import math


errorloglevel = logging.WARNING
logging.basicConfig(filename=k.errorfile, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

UPDATE_DELAY = 60 * 7


class DPhashtable:
    def __init__(self, posixtime):
        self.posix_time = posixtime
        self.values = []

    def avg_values(self):
        returnvalue = k.null_output_value
        if len(self.values) > 0:
            returnvalue = float(0)
            for i in range(0, len(self.values)):
                returnvalue = returnvalue + float(self.values[i])
            returnvalue = round((float(returnvalue) / len(self.values)),2)
        return returnvalue

    def posix2utc(self, posixvalue):
        utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        return utctime

    def print_values_posix(self):
        returnstring = str(self.posix_time) + "," + str(self.avg_values())
        return returnstring

    def print_values_utc(self):
        timestamp = self.posix2utc(self.posix_time)
        returnstring = str(timestamp) + "," + str(self.avg_values())
        return returnstring


# Set up the list of sensors here
logging.debug("Setting up magnetometer stations")

goes15 = MagGOES_16("GOES_15",
                            "Geostationary Orbit",
                            "NASA",
                            r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d",
                            "%Y-%m-%d %H:%M:%S",
                            1,
                            "https://services.swpc.noaa.gov/json/goes/secondary/magnetometers-6-hour.json")

def filter_median(array_to_parse):
    returnlist = []
    if len(array_to_parse) > 10:
        for i in range(1, len(array_to_parse)-1):
            datm = array_to_parse[i].posix_time
            filterwindow = []

            for j in range(-1, 2):
                filterwindow.append(array_to_parse[i+j].data)

            filterwindow.sort()
            data = filterwindow[1]
            dp = Datapoint(datm, data)
            returnlist.append(dp)
    return returnlist


def filter_dvdt(array_to_parse):
    returnlist = []
    for i in range(1, len(array_to_parse)):
        dvdt = float(array_to_parse[i].data) - float(array_to_parse[i-1].data)
        datm = array_to_parse[i].posix_time
        dp = Datapoint(datm, dvdt)
        returnlist.append(dp)
    return returnlist


def filter_deblip(dvdtdata, blipsize):
    returnarray = []
    for item in dvdtdata:
        testdata = math.sqrt(math.pow(item.data, 2))
        if testdata > blipsize:
            dp = Datapoint(item.posix_time, 0)
        else:
            dp = Datapoint(item.posix_time, item.data)
        returnarray.append(dp)
    return returnarray


def filter_reconstruction(startvalue, dvdtlist):
    returnlist = []
    currentdata = startvalue
    for item in dvdtlist:
        datm = item.posix_time
        currentdata = float(currentdata) + float(item.data)
        dp = Datapoint(datm, currentdata)
        returnlist.append(dp)
    return returnlist


def filter_hashtable(datapoint_values, binvalue):
    starttime = int(time()) - (24*60*60)
    hashlist = []

    for i in range(starttime, int(time()), binvalue):
        dp = DPhashtable(i)
        hashlist.append(dp)

    for item in datapoint_values:
        index = math.floor(((int(item.posix_time) - starttime) / binvalue))
        try:
            hashlist[index].values.append(item.data)
        except IndexError:
            print("Index error with instrument_manager.filter_hashtable()")
            logging.error("ERROR: Index error with instrument_manager.filter_hashtable()")

    return hashlist


def save_logfile(filename, data):
    """Save the current data to CSV logfile"""
    try:
        with open(filename, "w") as w:
            for data_point in data:
                w.write(data_point.print_values_utc() + "\n")
    except PermissionError:
        logging.error("ERROR: Permission error - unable to write logfile " + str(filename))


if __name__ == "__main__":
    # gather and record raw data for all instruments
    # for instrument in instrument_list:
    goes15.process_data()

    # process raw data to remove spikes, blips, etc, for display,
    # creation of indices, etc
    cleaned_data = []
    if len(goes15.array24hr) > 10:
        startvalue = goes15.array24hr[0].data
        filteredlist = filter_median(goes15.array24hr)
        # filteredlist = filter_dvdt(instrument.array24hr)
        # filteredlist = filter_deblip(filteredlist, goes16.blipsize)
        # # reconstructed_data = filter_reconstruction(startvalue, filteredlist)

        # apply a hash filter to convert all data to one minute intervals.
        # bins_1min = filter_hashtable(filteredlist, 60)
        cleanfile = "1mins_" + goes15.name + ".csv"
        save_logfile(cleanfile, filteredlist)


