import mgr_json_data
import mgr_solar_image
# import mgr_data
# import mgr_plotter
# import mgr_forecast
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


sun = mgr_solar_image.SolarImageProcessor("https://services.swpc.noaa.gov/images/animations/suvi/primary/195/latest.png")
#
# data_manager = mgr_data.DataManager(LOGFILE)
# forecaster = mgr_forecast.Forecaster()
# common_data.report_string = ""

def database_create():
    db = sqlite3.connect(common_data.database)
    cursor = db.cursor()
    cursor.execute("drop table if exists satellites;")
    cursor.execute("drop table if exists sw_data;")
    cursor.execute("drop table if exists imagedata;")
    cursor.execute("drop table if exists observations;")

    cursor.execute("create table satellites ("
                   "sat_id text primary key"
                   ");")

    cursor.execute('create table sw_data ('
                   'posix_obs_time integer primary key,'
                   'posix_launch_time integer,'
                   'speed real,'
                   'density real,'  
                   'sat_id text,'
                   'foreign key (sat_id) references satellites(sat_id)'
                   ');')

    cursor.execute('create table imagedata ('
                   'posixtime integer primary key,'
                   'pixel_coverage integer,'
                   'sat_id text,'
                   'foreign key (sat_id) references satellites(sat_id)'
                   ');')

    cursor.execute('create table observations ('
                   'posixtime integer,'
                   'posix_obs_time integer,'
                   'foreign key (posixtime) references imagedata(posixtime),'
                   'foreign key (posix_obs_time) references sw_data(posix_obs_time)'
                   ');')

    cursor.execute('insert into satellites (sat_id) '
                   'values ("goes_west");')

    cursor.execute('insert into satellites (sat_id) '
                   'values ("goes_east");')

    cursor.execute('insert into satellites (sat_id) '
                   'values ("dscovr");')

    db.commit()
    db.close()


def database_add_satdata(sat_data, recent_dt):
    db = sqlite3.connect(common_data.database)
    cursor = db.cursor()

    for item in sat_data:
        if item[0] > recent_dt:
            print(item)
            cursor.execute('insert into observations (datetime, speed, density, cover) '
                           'values (?,?,?,0);', item)
    db.commit()
    db.close()


def database_get_latest_dt():
    db = sqlite3.connect(common_data.database)
    cursor = db.cursor()
    cursor.execute('select max(datetime) from observations;')
    for item in cursor.fetchone():
        returnvalue = item
    db.close()
    return returnvalue


if __name__ == "__main__":
    # reset the resport string
    common_data.report_string = ""

    # Check database exists. If not create it.
    if os.path.isfile(common_data.database) is False:
        database_create()

    # # get the wind data and coronal hole coverage. In cases of no information, the returned values will be ZERO!
    # # Get the satellite data
    # sat_data = mgr_json_data.wrapper("http://services.swpc.noaa.gov/products/solar-wind/plasma-2-hour.json")
    # latest_stored_datetime = database_get_latest_dt()
    # database_add_satdata(sat_data, latest_stored_datetime)


    # process latest solar image
    # sun.get_meridian_coverage()

    # get current posix time and create the datapoint to append to main data
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

