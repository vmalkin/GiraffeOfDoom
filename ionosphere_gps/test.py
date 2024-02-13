import mgr_database
import mgr_plotter
import time

last_6_hours = time.time() - (60*60*12)
query_result = mgr_database.db_get_gsv(last_6_hours)
mgr_plotter.polarplot_paths(query_result)

# start = time.time() - (60*60*24)
# query_result = mgr_database.db_get_snr(start)
# mgr_plotter.basicplot(query_result)

