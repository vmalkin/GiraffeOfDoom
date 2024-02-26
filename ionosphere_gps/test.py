import mgr_database
import mgr_plotter
import time

print('Plot last hour GPS tracks')
last_6_hours = time.time() - (60 * 60 * 6)
query_result = mgr_database.db_get_gsv(last_6_hours, 1)
mgr_plotter.polarplot_paths(query_result)
mgr_plotter.snr_azimuth(query_result)
