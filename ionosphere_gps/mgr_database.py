import sqlite3
import constants as k


def db_create():
    # create database!
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()

    db.execute('drop table if exists observations;')

    db.execute('create table observations ('
               'constellation text,'
               'sat_id text,'
               'posixtime integer,'
               'alt integer,'
               'az integer,'
               'snr integer'
               ');')

    gpsdb.commit()
    db.close()


def db_gpgsv_add(gsvdata, constellation_id):
    # this method expects an array with each element in the array being:
    # [1707638483, '11', '01', '201', ''] (posix, satID, alt, az, snr)
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    for item in gsvdata:
        posixtime = item[0]
        # sat id must match IDs entered in satellites table.
        sat_id = convert_sat_id(item[1])
        alt = item[2]
        az = item[3]
        snr = item[4]
        values = [constellation_id, sat_id, posixtime, alt, az, snr]
        db.execute('insert into observations(constellation, sat_id, posixtime, alt, az, snr) '
                   'values (?, ?, ?, ?, ?, ?);', values)
    gpsdb.commit()
    db.close()


def db_get_gsv(timestart, altitude):
    returnarray = []
    values = [timestart, altitude]
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select * from observations where posixtime > ? and alt > ?'
                        'order by sat_id asc, posixtime asc ', values)
    for item in result:
        returnarray.append(item)
    db.close()
    return returnarray


def db_get_snr(timestart, altitude):
    returnarray = []
    values = [timestart, altitude]
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select posixtime, snr from observations where posixtime > ? '
                        'and alt > ?;', values)
    for item in result:
        returnarray.append(item)
    db.close()
    return returnarray


def convert_sat_id(id_num):
    index = str(id_num)
    if len(index) == 1:
        index = '0' + index
    id_num = index
    return id_num

def db_get_grouped_snr(timestart):
    returnarray = []
    values = [timestart]
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select posixtime, avg(snr) from observations '
                        'where posixtime > ? group by posixtime', values)
    for item in result:
        returnarray.append(item)
    db.close()
    return returnarray