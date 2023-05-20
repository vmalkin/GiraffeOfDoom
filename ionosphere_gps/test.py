import time
import mgr_database
import mgr_plot


start_time = int(time.time() - (5 * 24 * 60 * 60))

# Get data for each constellation.
result = mgr_database.qry_get_last_24hrs(start_time, "GPGGA")
mgr_plot.wrapper(result, "GPS")


