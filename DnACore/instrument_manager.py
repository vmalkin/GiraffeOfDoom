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
from instruments import MagnetometerWebCSV
from instruments import MagnetometerWebGOES
from instruments import Discovr_Bz_JSON
from instruments import Discovr_SolarWind_JSON
from instruments import CSVFile_Windspeed
from instruments import CSVFile_Density

from time import sleep, time
import datetime
import constants as k
import processor
import logging
import math
import os


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

rapid_run = MagnetometerWebCSV("Ruru_Rapidrun",
                               "Dunedin",
                               "Ruru Observatory",
                               r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d",
                               "%Y-%m-%d %H:%M:%S",
                               1,
                               "http://www.ruruobservatory.org.nz/dr01_1hr.csv")

induction = MagnetometerWebCSV("Induction_GIC",
                               "Dunedin",
                               "Dunedin Aurora",
                               r"\d\d\d\d-\d\d-\d\d \d\d:\d\d",
                               "%Y-%m-%d %H:%M",
                               9,
                               "http://www.ruruobservatory.org.nz/induction_gic.csv")

goes1 = MagnetometerWebGOES("GOES_Primary",
                            "Geostationary Orbit",
                            "NASA",
                            r"\d\d\d\d-\d\d-\d\d \d\d:\d\d",
                            "%Y-%m-%d %H:%M",
                            1,
                            "http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt")

goes2 = MagnetometerWebGOES("GOES_Secondary",
                            "Geostationary Orbit",
                            "NASA",
                            r"\d\d\d\d-\d\d-\d\d \d\d:\d\d",
                            "%Y-%m-%d %H:%M",
                            1,
                            "https://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt")

proxy_solarwind = Discovr_SolarWind_JSON("DISCOVR solar wind","","","","",9,
                              "https://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json")

ds_windspeed = CSVFile_Windspeed("sw_speed",
                                 "",
                                 "NASA",
                                 r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d",
                                 "%Y-%m-%d %H:%M:%S.%f",
                                 9,
                                 "discovr_solarwind_json.csv")

ds_winddens = CSVFile_Density("sw_density",
                                 "",
                                 "NASA",
                                 r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d",
                                 "%Y-%m-%d %H:%M:%S.%f",
                                 9,
                                 "discovr_solarwind_json.csv")


dscovr_bz = Discovr_Bz_JSON("DISCOVR_Bz",
                              "Geostationary Orbit",
                              "NASA",
                              r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d",
                              "%Y-%m-%d %H:%M:%S.%f",
                            9,
                              "https://services.swpc.noaa.gov/products/solar-wind/mag-2-hour.json")

logging.debug("appending to list")
instrument_list = []

try:
    instrument_list.append(rapid_run)
except:
    logging.WARNING("Unable to load Ruru Observatory")
    print("Unable to load Ruru Observatory")

try:
    instrument_list.append(induction)
except:
    logging.WARNING("Unable to load induction coil data")
    print("Unable to load induction coil data")

try:
    instrument_list.append(goes1)
except:
    logging.WARNING("Unable to load GOES 1")
    print("Unable to load GOES 1")

try:
    instrument_list.append(goes2)
except:
    logging.WARNING("Unable to load GOES 2")
    print("Unable to load GOES 2")

try:
    instrument_list.append(dscovr_bz)
except:
    logging.WARNING("Unable to load DISCOVR")
    print("Unable to load DISCOVR")

solarwind_list = []
try:
    solarwind_list.append(proxy_solarwind)
except:
    logging.WARNING("Unable to load proxy solar wind data")
    print("Unable to load DISCOVR")

try:
    solarwind_list.append(ds_windspeed)
except:
    logging.WARNING("Unable to load solar wind speed")
    print("Unable to load DISCOVR")

try:
    solarwind_list.append(ds_winddens)
except:
    logging.WARNING("Unable to load solar wind density")
    print("Unable to load DISCOVR")

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
        index = int((int(item.posix_time) - starttime) / binvalue) - 1
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
    while True:
        # gather and record raw data for all instruments
        # for instrument in instrument_list:
        instrument.process_data()

        # process raw data to remove spikes, blips, etc, for display,
        # creation of indices, etc
        cleaned_data = []
        for instrument in instrument_list:
            if len(instrument.array24hr) > 10:
                startvalue = instrument.array24hr[0].data
                # filteredlist = filter_median(instrument.array24hr)
                filteredlist = filter_dvdt(instrument.array24hr)
                filteredlist = filter_deblip(filteredlist, instrument.blipsize)
                reconstructed_data = filter_reconstruction(startvalue, filteredlist)

                # apply a hash filter to convert all data to one minute intervals.
                bins_1min = filter_hashtable(reconstructed_data, 60)
                cleanfile = "1mins_" + instrument.name + ".csv"
                save_logfile(cleanfile, bins_1min)

                # Save reconstructed data here to perform analysis
                # GOES data still seems to be off, but the shape is more consistent
                new_dp = [instrument.name, bins_1min]
                cleaned_data.append(new_dp)

        # Process the solar wind data separatly
        for instrument in solarwind_list:
            instrument.process_data()
            if len(instrument.array24hr) > 10:
                # startvalue = instrument.array24hr[0].data
                filteredlist = filter_median(instrument.array24hr)
                # filteredlist = filter_dvdt(instrument.array24hr)
                # filteredlist = filter_deblip(filteredlist, instrument.blipsize)
                # reconstructed_data = filter_reconstruction(startvalue, filteredlist)

                # apply a hash filter to convert all data to one minute intervals.
                bins_1min = filter_hashtable(filteredlist, 60)
                cleanfile = "1mins_" + instrument.name + ".csv"
                save_logfile(cleanfile, bins_1min)

            processor.average_20mins(instrument.name, instrument.array24hr)

        #Done! wait for next iteration
        print("\nUpdate completed...")
        for i in range(0, UPDATE_DELAY):
            print(str(UPDATE_DELAY - i) + " seconds until next pass")
            sleep(1)
