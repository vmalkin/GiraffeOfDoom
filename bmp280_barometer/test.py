import mgr_database
import mgr_matplot
import time
import os
import constants as k

now = int(time.time())
timeinterval = now - (60 * 60 * 6)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "pressure_24.png"
print("Plot pressure 25 hours")
mgr_matplot.plot_time_data(queryresult, savefile)

# savefile = k.dir_images + os.sep + "dxdt.png"
# mgr_matplot.plot_time_dxdt(queryresult, savefile)

# savefile = k.dir_images + os.sep + "detrended_24.png"
# halfwindow = 60 * 2.5
# print("Plot detrended pressure 25 hours")
# mgr_matplot.plot_detrended(queryresult, halfwindow, savefile)

