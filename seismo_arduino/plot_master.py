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
import plotter_fft_7d
import plotter_fft_movie
import mgr_emd
import os


def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


print(f'Querying database...')
time_end = time.time()
time_start_7d = time_end - (60 * 60 * 24 * 7)
# result_total = mgr_database.db_data_get_all()
result_7d = mgr_database.db_data_get(time_start_7d)
result_1d = result_7d[-86400 * int(1 / k.sensor_reading_frequency):]
print(f'Query Complete.')
print(f'Begin plotting...')

for key in k.dir_images:
    try_create_directory(key)

# plotter_phaseportrait.wrapper(result_1d)
# plotter_spectrograms.wrapper((result_1d))
plotter_combo1day.wrapper(result_1d)
plotter_combo7day.wrapper(result_7d)
# plotter_dual.wrapper(result_1d)
# plotter_helicorder.wrapper(result_1d)
# plotter_fft_7d.wrapper(result_7d)
# plotter_fft_movie.wrapper(result_1d)

# # Run this only on an offline database!
# alldata = mgr_database.db_data_get_all()
# plotter_combo7day.wrapper(alldata)

# # =============================================================================================================
# # Empirical Mode Decomposition
# print("Empirical Mode Decomposition")
# aggregate_array = result_1d
# aggregate_array.pop(0)
# plot_utc = []
# plot_seismo = []
# wrapperdata = []
#
# for i in range(1, len(aggregate_array)):
#     tim = aggregate_array[i][0]
#     tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
#     siz = aggregate_array[i][1]
#     plot_utc.append(tim)
#     plot_seismo.append(siz)
#
# wrapperdata.append(plot_utc)
# wrapperdata.append(plot_seismo)
# savefile = k.dir_images['images'] + os.sep + "imf.png"
# df = "%d  %H:%M"
# mgr_emd.wrapper(wrapperdata, savefile, df)

timefinish = time.time()
print(f"Plotting complete. Elapsed minutes to process: {(timefinish - time_end) / 60}")
