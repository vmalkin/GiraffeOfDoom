import mgr_plot_diurnal
import mgr_plot_diffs
import mgr_emd
import mgr_plot_detrended
import constants as k
import standard_stuff
import sqlite3
import time

starttime = 0
station_id = k.station_id
database = "temp.db"
filename = "dr01_24hr.csv"
publish_dir = k.publish_dir

gpsdb = sqlite3.connect(database)
# gpsdb = sqlite3.connect(":memory:")
db = gpsdb.cursor()
db.execute('drop table if exists data;')
db.execute('create table data ('
           'posixtime text,'
           'datavalue real'
           ');')
gpsdb.commit()
db.close()

dataarray = []
with open(filename, "r") as dd:
    counter = 0
    for row in dd:
        if counter > 0:
            for row in dd:
                data = row.replace("\n", "")
                datasplit = data.split(",")
                posixtime = standard_stuff.utc2posix(datasplit[0], '%Y-%m-%d %H:%M:%S')
                reading = datasplit[1]
                dp = [int(posixtime) , float(reading)]
                dataarray.append(dp)

        counter = counter + 1

db = sqlite3.connect(database)
cursor = db.cursor()
for i in range(0, len(dataarray)):
    cursor.execute("insert into data (posixtime, datavalue) values (?,?);", [dataarray[i][0], dataarray[i][1]] )
    if i / 1000 == 0:
        pcent = round((i / 1000), 2)
        print("Completion: ", pcent)
    db.commit()
db.close()

mgr_plot_diurnal.wrapper(database, 0, publish_dir)
mgr_plot_diffs.wrapper(database, 0, publish_dir)
mgr_plot_detrended.wrapper(database, 0, publish_dir)
mgr_emd.wrapper(database, 0, publish_dir)
