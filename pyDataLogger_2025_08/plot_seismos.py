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

index = 60 * 60 * 24 * 5
result_24hr = result_7d[-index:]

print(f"Number of records: {len(result_7d)}")
# ========================================================================================
# Examine the format of the returned data. We might need to split this off into a 24 hour
# section for passing directly into spectrographic analysis without any aggregating
# and another section for 24 hour, 7 Day, etc display of smoothed data with less detail
# so it renders faster in the plotting.
# ========================================================================================

# ========================================================================================
# Aggregate to compact data readings from every 0.1 seconds to every hour.
# ========================================================================================
aggregate_array = []
# the size of the window in seconds. must be more than zero
window = 60 * 60  # one hour

# PASS 1 - Set up the array
print("Setting up aggregating array")
date_start = 0
for i in range(0, len(result_7d), window):
    date_end = result_7d[i][0]
    d = class_aggregator.Aggregator(date_start, date_end)
    aggregate_array.append(d)
    date_start = date_end

# PASS 2 - generate the lookup array to speed up data placement
print("Generating lookup dict")
lookup = {}
j = 0
for i in range(0, len(result_7d)):
    key = (result_7d[i][0])
    value = (j)
    lookup[key] = value
    if i % window == 0:
        j = j + 1

# PASS 3 - add the data into the correct aggregate object based on datetime
print("Adding data to aggregating array")
for i in range(0, len(result_7d)):
    # if i % 1000 == 0:
    #     print(f"{i} / {len(result_7d)}")
    datetime = result_7d[i][0]
    data = result_7d[i][1]
    agg_index = lookup[datetime]
    aggregate_array[agg_index - 1].data_values.append(data)

plotting_data = []
for item in aggregate_array:
    d = [item.get_avg_posix(), item.get_data_avg()]
    plotting_data.append(d)

utc_datelist_7d = []
seismo_data_7d = []
for item in plotting_data:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist_7d.append(utc)
    seismo_data_7d.append(seismo)

print("Tiltmeter - 7 day")
savefile = k.dir_images + os.sep + "seven_day.png"
mgr_matplot.plot_time_data(utc_datelist_7d, seismo_data_7d, 64,"Tiltmeter 7 Days", savefile)


# ========================================================================================
# Aggregate to compact data readings to every 2 seconds
# ========================================================================================
aggregate_array = []
# the size of the window in seconds. must be more than zero
window = 2

# PASS 1 - Set up the array
print("Setting up aggregating array")
date_start = 0
for i in range(0, len(result_24hr), window):
    date_end = result_7d[i][0]
    d = class_aggregator.Aggregator(date_start, date_end)
    aggregate_array.append(d)
    date_start = date_end

# PASS 2 - generate the lookup array to speed up data placement
print("Generating lookup dict")
lookup = {}
j = 0
for i in range(0, len(result_24hr)):
    key = (result_24hr[i][0])
    value = (j)
    lookup[key] = value
    if i % window == 0:
        j = j + 1

# PASS 3 - add the data into the correct aggregate object based on datetime
print("Adding data to aggregating array")
for i in range(0, len(result_24hr)):
    # if i % 1000 == 0:
    #     print(f"{i} / {len(result_24hr)}")
    datetime = result_24hr[i][0]
    data = result_24hr[i][1]
    agg_index = lookup[datetime]
    aggregate_array[agg_index - 1].data_values.append(data)


plotting_data = []
for item in aggregate_array:
    d = [item.get_avg_posix(), item.get_data_avg()]
    plotting_data.append(d)

utc_datelist_24 = []
seismo_data_24 = []
for item in plotting_data:
    utc = standard_stuff.posix2utc(item[0], '%Y-%m-%d %H:%M:%S.%f')
    seismo = item[1]
    utc_datelist_24.append(utc)
    seismo_data_24.append(seismo)

print("Tiltmeter - Past 24 hours")
savefile = k.dir_images + os.sep + "one_day.png"
mgr_matplot.plot_time_data(utc_datelist_24, seismo_data_24, 30000,"Tiltmeter One Day", savefile)

print("Tiltmeter Spectrogram - Past 24 hours")
savefile = k.dir_images + os.sep + "spectrum.png"
mgr_matplot.plot_spectrum(seismo_data_24, utc_datelist_24, savefile)

print("Tiltmeter - hourly")
mgr_matplot.plot_hourly_array(utc_datelist_24, seismo_data_24, k.dir_images)

