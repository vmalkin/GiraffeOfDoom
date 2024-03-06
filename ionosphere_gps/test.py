import mgr_database
import mgr_plotter
import time

print("***************************** Start Query Processor")
now = int(time.time())

# print('Plot last hour GPS tracks')
# last_6_hours = now - (60 * 60 * 6)
# query_result = mgr_database.db_get_gsv(last_6_hours, 1)
# mgr_plotter.polarplot_paths(query_result)
#
# print('Plot SNR vs Azimuth')
# mgr_plotter.snr_azimuth(query_result)

print('Plot Average SNR')
start = now - (60 * 60 * 24)
query_result = mgr_database.db_get_gsv(start, 20)
mgr_plotter.avg_snr_time(now, start, query_result)

print("******************************* End Query Processor")
