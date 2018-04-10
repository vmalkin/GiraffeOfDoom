import mgr_discovr_data
import mgr_solar_image
import mgr_data
import time
LOGFILE = 'log.csv'
__version__ = '0.8'
__author__ = "Vaughn Malkin"

discovr = mgr_discovr_data.SatelliteDataProcessor()
sun = mgr_solar_image.SolarImageProcessor()
data_manager = mgr_data.DataManager(LOGFILE)

if __name__ == "__main__":
    while True:
        discovr.get_data()
        sun.get_meridian_coverage()

        # sun.coverage  discovr.wind_speed  discovr.wind_density

        # Pause for an hour
        time.sleep(3600)

