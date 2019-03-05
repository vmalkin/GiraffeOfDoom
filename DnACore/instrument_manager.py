"""
This is the instrument manager for Dunedin Aurora.

logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
from instruments import MagnetometerLocalCSV, MagnetometerURL
import time
import constants as k
import logging

errorloglevel = logging.DEBUG
logging.basicConfig(filename=k.errorfile, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

UPDATE_DELAY = 300

# Set up the list of sensors here
logging.debug("Setting up magnetometer stations")
rapid_run = MagnetometerLocalCSV("Ruru_Rapidrun", "Vaughn", "Dunedin", "NULL", "C://test.csv")
goes = MagnetometerURL("GOES", "Vaughn", "Dunedin", "NULL", "http://www.test.com")

logging.debug("appending to list")
instrument_list = []
instrument_list.append(rapid_run)
instrument_list.append(goes)

if __name__ == "__main__":
    while True:
        for instrument in instrument_list:
            instrument.process_data()

        print("\nUpdate completed...")
        for i in range(0, UPDATE_DELAY):
            print(str(UPDATE_DELAY - i) + " seconds until next pass")
            time.sleep(1)