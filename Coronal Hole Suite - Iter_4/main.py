import mgr_json_data
import mgr_solar_image
import mgr_data
import mgr_plotter
import mgr_forecast
import time
import common_data

import sqlite3
import os


# LOGFILE = common_data.reading_actual
# WAITPERIOD = 86400 * 5
__version__ = '4.0'
__author__ = "Vaughn Malkin"

# self._save_image_from_url("https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg", "sun.jpg")
# self._save_image_from_url("https://services.swpc.noaa.gov/images/suvi-primary-195.png", "sun.jpg")
# self._save_image_from_url("https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png", "sun.jpg")
# solar wind data json http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json

# discovr = mgr_json_data.SatelliteDataProcessor("http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json")
# sun = mgr_solar_image.SolarImageProcessor("https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png")
#
# data_manager = mgr_data.DataManager(LOGFILE)
# forecaster = mgr_forecast.Forecaster()
# common_data.report_string = ""

def database_create():
    db = sqlite3.connect(common_data.database)
    cursor = db.cursor()
    cursor.execute()

    db.commit()
    db.close()


if __name__ == "__main__":
    # while True:
    # reset the resport string
    common_data.report_string = ""

    # Check database exists. If not create it.
    if os.path.isfile(common_data.database) is False:
        database_create()






    # # get the wind data and coronal hole coverage. In cases of no information, the returned values will be ZERO!
    # # Get the satellite data
    # discovr.get_data()
    #
    # # process latest solar image
    # sun.get_meridian_coverage()
    #
    # # get current posix time and create the datapoint to append to main data
    # posixtime = int(time.time())   # sun.coverage  discovr.wind_speed  discovr.wind_density
    # dp = mgr_data.DataPoint(posixtime, sun.coverage, discovr.wind_speed, discovr.wind_density)
    # print(dp.return_values())
    #
    # # append the new datapoint and process the master datalist
    # data_manager.append_datapoint(dp)
    # data_manager.process_new_data()
    #
    # # Calculate if enough time has elapsed to start running the forecasting.
    # startdate = int(data_manager.master_data[0].posix_date)
    # nowdate = int(data_manager.master_data[len(data_manager.master_data) - 1].posix_date)
    # elapsedtime = nowdate - startdate
    # timeleft = (WAITPERIOD - elapsedtime) / (60 * 60 * 24)
    #
    # if elapsedtime >= WAITPERIOD:
    #     # create the forecast
    #     forecaster.calculate_forecast(data_manager.master_data)
    #
    #     # Instantiate the prediction plotter, this will load it with the lates values. Plot the final data
    #     prediction_plotter = mgr_plotter.Plotter()
    #     prediction_plotter.plot_data()
    # else:
    #     common_data.report_string = common_data.report_string + ("<br>Insufficient time has passed to begin forecasting. " + str(timeleft)[:5] + " days remaining" + "\n")
    #     print(common_data.report_string)
    #     with open(common_data.regression_ouput, 'w') as w:
    #         w.write(common_data.report_string + '\n')
    #
    #     # Pause for an hour
    #     # time.sleep(3600)

