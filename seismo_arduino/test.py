import mgr_database
import time
import constants as k
from datetime import datetime, timezone
import plotter_phaseportrait
import plotter_spectrograms
import plotter_combo1day
import plotter_combo7day
import plotter_dual
import plotter_helicorder
import mgr_emd
import os

print(f'Querying database...')
time_end = time.time()
time_start_7d = time_end - (60 * 60 * 24 * 7)
# result_total = mgr_database.db_data_get_all()
result_7d = mgr_database.db_data_get(time_start_7d)
result_1d = result_7d[-86400 * int(1 / k.sensor_reading_frequency):]
print(f'Query Complete.')
print(f'Begin plotting...')

plotter_helicorder.wrapper(result_1d)

