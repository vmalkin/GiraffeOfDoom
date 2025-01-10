import mgr_database
import mgr_matplot
import time
import os
import constants as k

print("***************************** Start Query Processor")
now = int(time.time())

print('Plot last 24 hour GPS tracks')
now = int(time.time())
timeinterval = now - (60 * 60 * 12)
query_result = mgr_database.db_get_gsv(timeinterval, 1)

savefile = k.dir_images + os.sep + "simple_polar_snr.png"
mgr_matplot.plot_polar_noise(query_result, savefile)
print("******************************* End Query Processor")
