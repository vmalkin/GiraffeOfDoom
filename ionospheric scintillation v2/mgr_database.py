import sqlite3
import constants as k

db = k.sat_database

def database_create():
    print("No database, creating file")
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists satdata;')
    db.execute('create table satdata ('
               'comport_id text,'
               'sat_id text,'
               'posixtime integer,'
               'visible_sats integer,'
               'alt real,'
               'az real,'
               'snr real'
               ');')
    gpsdb.commit()
    db.close()

def qry_get_last_24hrs(starttime, altitude):
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select * from satdata where posixtime > ? and alt > ? order by posixtime asc;', [starttime, altitude])
    returnarray = []
    for item in result:
        dp = str(item[1]) + "," + str(item[2]) + "," + str(item[3]) + "," + str(item[4]) + "," + str(item[5])
        returnarray.append(dp)
    gpsdb.commit()
    db.close()
    return returnarray
