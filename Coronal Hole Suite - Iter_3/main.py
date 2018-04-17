import mgr_discovr_data
import mgr_solar_image
import mgr_data
import mgr_plotter
import mgr_forecast
import time

LOGFILE = 'log.csv'
WAITPERIOD = 86400 * 5
__version__ = '1.0'
__author__ = "Vaughn Malkin"

discovr = mgr_discovr_data.SatelliteDataProcessor()
sun = mgr_solar_image.SolarImageProcessor()
data_manager = mgr_data.DataManager(LOGFILE)
forecaster = mgr_forecast.Forecaster()

if __name__ == "__main__":
    while True:
        # get the wind data and coronal hole coverage. In cases of no information, the the
        # returned values will be ZERO!
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
            # create the forecast
            forecaster.calculate_forecast(data_manager.master_data)

            # Instantiate the prediction plotter, this will load it with the lates values. Plot the final data
            prediction_plotter = mgr_plotter.Plotter()
            prediction_plotter.plot_data()
        else:
            regression_status = ("Insufficient time has passed to begin forecasting. " + str(timeleft)[:5] + " days remaining")
            print(regression_status)
            with open("regression.php", 'w') as w:
                w.write(regression_status + '\n')

        # Pause for an hour
        time.sleep(3600)

