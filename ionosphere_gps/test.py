import mgr_database
import mgr_matplot
import time
import os
import constants as k

now = int(time.time())
timeinterval = now - (60 * 60 * 24 * 1)
query_result = mgr_database.db_get_gsv(timeinterval, 15)
print(query_result)

print("Plot avg SNR")
timeinterval = now - (60 * 60 * 24)
# queryresult = mgr_database.db_get_grouped_snr(timeinterval)
savefile = k.dir_images + os.sep + "simple_polar.png"
mgr_matplot.plot_polar_noise(query_result, savefile)

savefile = k.dir_images + os.sep + "simple_time_snr.png"
mgr_matplot.plot_time_snr(query_result, savefile)