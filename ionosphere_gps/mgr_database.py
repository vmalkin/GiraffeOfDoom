import sqlite3
import time

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
        id_num = convert_sat_id(i, 'GP')
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
        sat_id = convert_sat_id(item[1], 'GP')
        alt = item[2]
        az = item[3]
        snr = item[4]
        values = [sat_id, posixtime, alt, az, snr]
        db.execute('insert into observations(sat_id, posixtime, alt, az, snr) '
                   'values (?, ?, ?, ?, ?);', values)
    gpsdb.commit()
    db.close()


def db_get_avgsnr(timestart, altitude):
    returnarray = []
    values = [timestart, altitude]
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select snr from observations where posixtime > ? and alt > ?', values)
    for item in result:
        returnarray.append(item[0])
    return returnarray


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

def db_get_snr(timestart):
    returnarray = []
    values = [timestart]
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select posixtime, snr from observations where posixtime > ? '
                        'and alt > 20;', values)
    for item in result:
        returnarray.append(item)
    db.close()
    return returnarray

def db_get_latest_sats():
    returnarray = []
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select sat_id, max(posixtime) from observations group by sat_id;')
    for item in result:
        returnarray.append(item)
    db.close()
    return returnarray

def convert_sat_id(id_num, constellation):
    index = str(id_num)
    if len(index) == 1:
        index = '0' + index
    id_num = constellation + index
    return id_num