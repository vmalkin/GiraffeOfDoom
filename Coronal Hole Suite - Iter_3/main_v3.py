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
        # Get the satellite data
        discovr.get_data()

        # process latest solar image
        sun.get_meridian_coverage()

        # get current posix time and create the datapoint to append the the main data
        posixtime = int(time.time())
        # sun.coverage  discovr.wind_speed  discovr.wind_density
        dp = mgr_data.DataPoint(posixtime, sun.coverage, discovr.wind_speed, discovr.wind_density)
        print(dp.return_values())
        data_manager.append_datapoint(dp)
        data_manager.process_new_data()

        # Pause for an hour
        time.sleep(3600)

