import mgr_discovr_data
import mgr_solar_image
import mgr_data
import mgr_forecast
import time
LOGFILE = 'log.csv'
WAITPERIOD = 86400 * 5
__version__ = '0.8'
__author__ = "Vaughn Malkin"

discovr = mgr_discovr_data.SatelliteDataProcessor()
sun = mgr_solar_image.SolarImageProcessor()
data_manager = mgr_data.DataManager(LOGFILE)
forecaster = mgr_forecast.Forecaster()

if __name__ == "__main__":
    while True:
        # Get the satellite data
        discovr.get_data()

        # process latest solar image
        sun.get_meridian_coverage()

        # get current posix time and create the datapoint to append the the main data
        posixtime = int(time.time())   # sun.coverage  discovr.wind_speed  discovr.wind_density
        dp = mgr_data.DataPoint(posixtime, sun.coverage, discovr.wind_speed, discovr.wind_density)
        print(dp.return_values())

        # append the new datapoint and process the master datalist
        data_manager.append_datapoint(dp)
        data_manager.process_new_data()

        # Calculate if enough time has elapsed to start running the forecasting.
        startdate = int(data_manager.master_data[0].posix_date)
        nowdate = int(data_manager.master_data[len(data_manager.master_data) - 1].posix_date)
        elapsedtime = nowdate - startdate
        timeleft = (WAITPERIOD - elapsedtime) / (60 * 60 * 24)

        if elapsedtime >= WAITPERIOD:
            forecaster.calculate_forecast(data_manager.master_data)

        else:
            print("Insufficient time has passed to begin forecasting. " + str(timeleft)[:5] + " days remaining")

        # Pause for an hour
        time.sleep(3600)

