import mgr_database
import mgr_plotter
import time

# print('Plot last hour GPS tracks')
# last_6_hours = time.time() - (60 * 60 * 6)
# query_result = mgr_database.db_get_gsv(last_6_hours, 1)
# mgr_plotter.polarplot_paths(query_result)
# mgr_plotter.snr_azimuth(query_result)

# ('GP', '03', 1708928950, 59, 306, 30)
now = int(time.time())
start = now - (60 * 60 * 24)
query_result = mgr_database.db_get_gsv(start, 20)
print(query_result[30])
mgr_plotter.avg_snr_time(now, start, query_result)
