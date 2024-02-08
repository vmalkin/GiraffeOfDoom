import sqlite3
import constants as k

db = k.sat_database

def database_create():
    # $GPGGA, 223358.00, 4552.29314, S, 17029.06960, E, 1, 05, 1.74, 198.4, M, 1.8, M,, *79
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists satdata;')
    db.execute('create table satdata ('
               'constellation text,'
               'posixtime integer,'
               'lat real,'
               'long real,'
               'position_fix integer,'
               'num_sats integer,'
               'hdop real,'
               'alt real'
               ');')
    gpsdb.commit()
    db.close()

# def qry_get_last_24hrs(starttime, constellation_label):
#     gpsdb = sqlite3.connect(k.sat_database)
#     db = gpsdb.cursor()
#     result = db.execute('select * from satdata where constellation like ? and posixtime > ? order by posixtime asc;', [constellation_label, starttime])
#     returnarray = []
#     for item in result:
#         dp = [str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6]), str(item[7])]
#         returnarray.append(dp)
#     gpsdb.commit()
#     db.close()
#     return returnarray
#
# def qry_add_data(constellation, posixtime, lat, long, position_fix, num_sats, hdop, alt):
#     values = [constellation, posixtime, lat, long, position_fix, num_sats, hdop, alt]
#     db = sqlite3.connect(k.sat_database)
#     cursor = db.cursor()
#     cursor.execute('insert into satdata (constellation, posixtime, lat, long, position_fix, num_sats, hdop, alt) '
#                             'values (?, ?, ?, ?, ?, ?, ?, ?);', values)
#     db.commit()
#     cursor.close()
#     db.close()
#     pass
