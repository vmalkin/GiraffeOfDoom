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