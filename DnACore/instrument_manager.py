"""
This is the instrument manager for Dunedin Aurora.

logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
from instruments import MagnetometerWebCSV, MagnetometerWebGOES, Discovr_Density_JSON
import time
import constants as k
import logging

errorloglevel = logging.WARNING
logging.basicConfig(filename=k.errorfile, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

UPDATE_DELAY = 300

# Set up the list of sensors here
logging.debug("Setting up magnetometer stations")
rapid_run = MagnetometerWebCSV("Ruru_Rapidrun", "Vaughn", "Dunedin", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d", "%Y-%m-%d %H:%M:%S", "http://www.ruruobservatory.org.nz/dr01_1hr.csv")
goes1 = MagnetometerWebGOES("GOES_Primary", "NASA", "Geostationary Orbit", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d", "%Y-%m-%d %H:%M", "http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt")
goes2 = MagnetometerWebGOES("GOES_Secondary", "NASA", "Geostationary Orbit", r"\d\d\d\d-\d\d-\d\d \d\d:\d\d", "%Y-%m-%d %H:%M", "https://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt")
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


if __name__ == "__main__":
    while True:
        for instrument in instrument_list:
            
            instrument.process_data()
            

        print("\nUpdate completed...")
        for i in range(0, UPDATE_DELAY):
            print(str(UPDATE_DELAY - i) + " seconds until next pass")
            time.sleep(1)