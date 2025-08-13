import mgr_database
import mgr_matplot
import time
import os
import constants as k
import standard_stuff
import class_aggregator

time_end = time.time()
time_start_7d = time_end - (60 * 60 * 24 * 7)
result_7d = mgr_database.db_get_pressure(time_start_7d)

# ========================================================================================
# Examine the format of the returned data. We might need to split this off into a 24 hour
# section for passing directly into spectrographic analysis without any aggregating
# and another section for 24 hour, 7 Day, etc display of smoothed data with less detail
# so it renders faster in the plotting.
# ========================================================================================

# utc_datelist_24hr = []
# seismo_data_24hr = []
# for item in result_24h:
#     utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
#     seismo = item[1]
#     utc_datelist_24hr.append(utc)
#     seismo_data_24hr.append(seismo)

utc_datelist_7d = []
seismo_data_7d = []
for item in result_7d:
    utc = item[0]
    seismo = item[1]
    utc_datelist_7d.append(utc)
    seismo_data_7d.append(seismo)

# ========================================================================================
# Aggregate to compact data readings from every 0.1 seconds to evey 1 min, or 5 mins, etc.
# Example in the class_aggregator file.
# ========================================================================================



# print("Tiltmeter - Past 24 hours")
# savefile = k.dir_images + os.sep + "1days_tilt.png"
# mgr_matplot.plot_time_data(filtered_utc_datelist, filtered_seismo_data, 30000,"Tiltmeter One Day", savefile)
#
# print("Tiltmeter Spectrogram - Past 24 hours")
# savefile = k.dir_images + os.sep + "spectrum.png"
# mgr_matplot.plot_spectrum(seismo_data_24hr, utc_datelist_24hr, savefile)
#
# print("Tiltmeter - 7 day")
# filter_window = 5 * 60 * 10
# filtered_seismo_data_7d = standard_stuff.filter_median(seismo_data_7d, filter_window)
# filtered_utc_datelist_7d = utc_datelist_7d[filter_window: -1 * filter_window]
# savefile = k.dir_images + os.sep + "7d_tilt.png"
# mgr_matplot.plot_time_data(filtered_utc_datelist_7d, filtered_seismo_data_7d, 30000,"Tiltmeter One Day", savefile)
#
# print("Tiltmeter - hourly")
# mgr_matplot.plot_hourly_array(filtered_utc_datelist, filtered_seismo_data, k.dir_images)

