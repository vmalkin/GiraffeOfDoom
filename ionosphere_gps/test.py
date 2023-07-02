import time
import mgr_database
import mgr_plot_v2 as plotter


start_time = int(time.time() - (3 * 24 * 60 * 60))

# Get data for each constellation.
result = mgr_database.qry_get_last_24hrs(start_time, "GPGGA")
plotter.wrapper(result, "GPS")


