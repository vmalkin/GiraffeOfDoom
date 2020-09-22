import os
import sqlite3

sat_database = "gps_satellites.db"


if os.path.isfile(sat_database) is False:
    print("False")
if os.path.isfile(sat_database) is True:
    print("True")

gpsdb = sqlite3.connect(sat_database)
db = gpsdb.cursor()
db.execute('drop table if exists satdata;')
msg = db.execute('create table satdata ('
    'sat_id text,'
    'posixtime integer,'
    'alt real,'
    'az real,'
    's4 real'
    ');')
gpsdb.commit()
db.close()


