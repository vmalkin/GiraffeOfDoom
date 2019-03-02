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
import logging

UPDATE_DELAY = 300

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

rapid_run = MagnetometerLocalCSV("Ruru Rapidrun", "Vaughn", "Dunedin", "NULL", "C://test.csv")
goes = MagnetometerURL("GOES", "Vaughn", "Dunedin", "NULL", "http://www.test.com")

instrument_list = []
instrument_list.append(rapid_run)
instrument_list.append(goes)

if __name__ == "__main__":
    while True:
        for instrument in instrument_list:
            instrument.get_data()
            instrument.append_new_data()
            instrument.prune_current_data()
            instrument.save_logfile()
            # instrument.calculate_dynamic_parameters()
            # instrument.save_dynamic_parameters()

        print("Update completed...")
        for i in range(0, UPDATE_DELAY):
            print(str(UPDATE_DELAY - i) + " seconds until next pass")
            time.sleep(1)