import sqlite3
import constants as k


def db_create():
    # create database!
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()

    db.execute('drop table if exists observations;')

    db.execute('create table observations ('
               'posixtime integer,'
               'seismodata real'
               ');')

    gpsdb.commit()
    db.close()


def db_data_add(gsvdata):
    # this method expects an array with each element in the array being:
    # [1737274820, '21.05', '99740.46'] (posixtime, temperature, pressure)
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    for item in gsvdata:
        posixtime = item[0]
        temperature = item[1]
        pressure = item[2]
        values = [posixtime, temperature, pressure]
        db.execute('insert into observations(posixtime, seismodata) '
                   'values (?, ?);', values)
    gpsdb.commit()
    db.close()


def db_get_pressure(timestart):
    returnarray = []
    values = [timestart]
    gpsdb = sqlite3.connect(k.sat_database)
    db = gpsdb.cursor()
    result = db.execute('select posixtime, seismodata from observations where posixtime > ?;', values)
    for item in result:
        returnarray.append(item)
    db.close()
    return returnarray

