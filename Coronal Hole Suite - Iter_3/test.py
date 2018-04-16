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


forecaster.calculate_forecast(data_manager.master_data)

# # Instantiate the prediction plotter, this will load it with the lates values. Plot the final data
# prediction_plotter = mgr_plotter.Plotter()
# prediction_plotter.plot_data()


