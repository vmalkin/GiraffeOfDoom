import mgr_database
import mgr_matplot
import time
import os
import constants as k
import standard_stuff

now = int(time.time())
timeinterval = now - (60 * 60 * 24 * 7)
queryresult = mgr_database.db_get_pressure(timeinterval)

with open('data.csv', 'w') as savedata:
    for line in queryresult:
        # print(line)
        dp = standard_stuff.posix2utc(line[0], '%Y-%m-%d %H:%M:%S')+ ',' + str(line[1]) + '\n'
        savedata.write(dp)

savefile = k.dir_images + os.sep + "7days_pressure.png"
print("Plot pressure seven days")
decimation = 60*5
mgr_matplot.plot_time_data(queryresult, decimation, savefile)

print("Plot dx-dt seven days")
savefile = k.dir_images + os.sep + "7days_dxdt.png"
mgr_matplot.plot_time_dxdt(queryresult, decimation, savefile)

print("Plot pressure one day")
timeinterval = now - (60 * 60 * 24)
queryresult = mgr_database.db_get_pressure(timeinterval)
savefile = k.dir_images + os.sep + "pressure_24.png"
decimation = 15
mgr_matplot.plot_time_data(queryresult, decimation, savefile)

# print("Plot dx-dt one day")
# savefile = k.dir_images + os.sep + "dxdt.png"
# mgr_matplot.plot_time_dxdt(queryresult, decimation, savefile)

print("Plot detrended pressure one day")
savefile = k.dir_images + os.sep + "detrended_24.png"
decimation = 15
halfwindow = int(60 / decimation) * 5
mgr_matplot.plot_detrended(queryresult, decimation, halfwindow, savefile)

