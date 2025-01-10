import mgr_database
import mgr_matplot
import time
import os
import constants as k

print("***************************** Start Query Processor")
now = int(time.time())

print('Plot last 24 hour GPS tracks')
last_6_hours = now - (60 * 60 * 6)
query_result = mgr_database.db_get_gsv(last_6_hours, 1)
# savefile = k.dir_images + os.sep + "simple_altaz.png"
# mgr_matplot.plot_alt_az(query_result, savefile)
#
# savefile = k.dir_images + os.sep + "simple_polar.png"
# mgr_matplot.plot_polar_positions(query_result, savefile)

savefile = k.dir_images + os.sep + "simple_polar_snr.png"
mgr_matplot.plot_polar_noise(query_result, savefile)
print("******************************* End Query Processor")
