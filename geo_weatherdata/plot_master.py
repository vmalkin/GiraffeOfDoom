import mgr_database
import time
import constants as k
from multiprocessing import Pool
import plotter_spectrum_baro
import os
from datetime import datetime, timezone

# def try_create_directory(directory):
#     if os.path.isdir(directory) is False:
#         print("Creating image file directory...")
#         try:
#             os.makedirs(directory)
#             print("Directory created.")
#         except:
#             if not os.path.isdir(directory):
#                 print("Unable to create directory")


print(f'Querying database...')
time_end = time.time()
# time_end = 1767870000
time_start_7d = time_end - (60 * 60 * 24 * 7)
# result_total = mgr_database.db_data_get_all()
result_7d = mgr_database.db_data_get(time_start_7d)
# result_1d = result_7d[-86400 * int(1 / k.sensor_reading_frequency):]
# result_1d = result_7d[-40000 * int(1 / k.sensor_reading_frequency):]
print(f'Query Complete.')
print(f'Begin plotting...')

plotter_spectrum_baro.wrapper(result_7d)

timefinish = time.time()
print(f"Plotting complete. Elapsed minutes to process: {(timefinish - time_end) / 60}")
