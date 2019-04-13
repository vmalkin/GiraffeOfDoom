"""
This is the instrument manager for Dunedin Aurora.

logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
from instruments import Datapoint, MagnetometerWebCSV, MagnetometerWebGOES, Discovr_Density_JSON
import time
import constants as k
import logging

errorloglevel = logging.WARNING
logging.basicConfig(filename=k.errorfile, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

UPDATE_DELAY = 300

# Set up the list of sensors here
logging.debug("Setting up magnetometer stations")
rapid_run = MagnetometerWebCSV("Ruru_Rapidrun", "Dunedin", "Ruru Observatory", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d", "%Y-%m-%d %H:%M:%S", "http://www.ruruobservatory.org.nz/dr01_1hr.csv")
goes1 = MagnetometerWebGOES("GOES_Primary", "Geostationary Orbit", "NASA", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d", "%Y-%m-%d %H:%M", "http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt")
goes2 = MagnetometerWebGOES("GOES_Secondary", "Geostationary Orbit", "NASA", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d", "%Y-%m-%d %H:%M", "https://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt")
dscovr = Discovr_Density_JSON("DISCOVR", "Geostationary Orbit", "NASA", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d", "%Y-%m-%d %H:%M:%S.%f", "https://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json")

logging.debug("appending to list")
instrument_list = []

try:
    instrument_list.append(rapid_run)
except:
    logging.WARNING("Unable to load Ruru Observatory")
    print("Unable to load Ruru Observatory")

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
    instrument_list.append(dscovr)
except:
    logging.WARNING("Unable to load DISCOVR")
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


def filter_reconstruction(startvalue, dvdtlist):
    returnlist = []
    currentdata = startvalue
    for item in dvdtlist:
        datm = item.posix_time
        currentdata = float(currentdata) + float(item.data)
        dp = Datapoint(datm, currentdata)
        returnlist.append(dp)
    return returnlist


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
        for instrument in instrument_list:
            instrument.process_data()

        for instrument in instrument_list:
            if len(instrument.array24hr) > 10:
                startvalue = instrument.array24hr[0].data
                cleanfile = "clean_" + instrument.name + ".csv"
                filteredlist = filter_median(instrument.array24hr)
                filteredlist = filter_dvdt(filteredlist)
                filteredlist = filter_median(filteredlist)
                reconstructed_data = filter_reconstruction(startvalue, filteredlist)
                save_logfile(cleanfile, reconstructed_data)

        print("\nUpdate completed...")
        for i in range(0, UPDATE_DELAY):
            print(str(UPDATE_DELAY - i) + " seconds until next pass")
            time.sleep(1)
