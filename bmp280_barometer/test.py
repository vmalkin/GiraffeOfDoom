import mgr_database
import mgr_matplot
import time
import os
import constants as k

now = int(time.time())
timeinterval = now - (60 * 60 * 24)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "long_term.png"
mgr_matplot.plot_time_data(queryresult, savefile)

# savefile = k.dir_images + os.sep + "dxdt.png"
# mgr_matplot.plot_time_dxdt(queryresult, savefile)

savefile = k.dir_images + os.sep + "detrended.png"
halfwindow = 60 * 5
mgr_matplot.plot_detrended(queryresult, halfwindow, savefile)

