import sqlite3
import constants as k

def db_create():
    # create database!
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    db.execute('drop table if exists constellation;')
    db.execute('drop table if exists satellites;')
    db.execute('drop table if exists observations;')
    db.execute('drop table if exists gga;')

    db.execute('create table constellation ('
               'constellation_id text primary key'
               ');')

    db.execute('create table satellite('
               'sat_id text primary key,'
               'constellation_id text,'
               'foreign key (constellation_id) references constellation(constellation_id)'
               ');')

    db.execute('create table observations ('
               'sat_id text,'
               'posixtime integer,'
               'alt integer,'
               'az integer,'
               'snr integer,'
               'foreign key (sat_id) references satellite(sat_id)'
               ');')

    db.execute('create table gga ('
               'constellation_id text,'
               'posixtime integer,'
               'lat real,'
               'long real,'
               'sats_used integer,'
               'hdop real,'
               'foreign key (constellation_id) references constellation(constellation_id)'
               ');')

    gpsdb.commit()
    db.close()


def db_initialise():
    # populate database with initial values
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()

    values = ['gps']
    db.execute('insert into constellation(constellation_id) values (?);', values)

    # for GPS satellites, usually only numbered 1 to 32
    for i in range(1, 33):
        id_num = convert_satID(i, 'GP')
        values = [id_num, 'gps']
        db.execute('insert into satellite(sat_id, constellation_id) values (?, ?);', values)
    # for GLONASS satellites?

    gpsdb.commit()
    db.close()

def db_gpgsv_add(gsvdata):
    # this method expects an array with each element in the array being:
    # [1707638483, '11', '01', '201', ''] (posix, satID, alt, az, snr)
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    for item in gsvdata:
        posixtime = item[0]
        # sat id must match IDs entered in satellites table.
        sat_id = convert_satID(item[1], 'GP')
        alt = item[2]
        az  = item[3]
        snr = item[4]
        values = [sat_id, posixtime, alt, az, snr]
        db.execute('insert into observations(sat_id, posixtime, alt, az, snr) '
                   'values (?, ?, ?, ?, ?);', values)
    gpsdb.commit()
    db.close()


def convert_satID(idNum, constellation):
    index = str(idNum)
    if len(index) == 1:
        index = '0' + index
    id_num = constellation + index
    return id_num

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
