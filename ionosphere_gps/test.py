import mgr_database
import mgr_plotter
import time


# print('Plot SNR vs Time')
start = time.time() - (60 * 60 * 24 * 5)
# query_result = mgr_database.db_get_snr(start)
# mgr_plotter.snr_time(query_result)
mgr_database.db_get_avgsnr(start, 20)
