import sqlite3
import constants as k


def db_create():
    # create database!
    gpsdb = sqlite3.connect(k.database)
    db = gpsdb.cursor()

    db.execute('drop table if exists observations;')

    db.execute('create table observations ('
               'posixtime real,'
               'temperature real,'
               'pressure real'
               ');')
    gpsdb.commit()
    db.close()


def db_data_add(gsvdata):
    # this method expects an array with each element in the array being:
    # [1737274820, '21.05', '99740.46'] (posixtime, temperature, pressure)
    try:
        gpsdb = sqlite3.connect(k.database, timeout=10)
        db = gpsdb.cursor()
        for item in gsvdata:
            posixtime = item[0]
            temperature = item[1]
            pressure = item[2]
            values = [posixtime, temperature, pressure]
            db.execute('insert into observations(posixtime, temperature, pressure) '
                       'values (?, ?, ?);', values)
        gpsdb.commit()
        db.close()
    except sqlite3.OperationalError:
        print(f'Database data insert FAILED - database locked')


def db_data_get(timestart):
    returnarray = []
    values = [timestart]
    try:
        gpsdb = sqlite3.connect(k.database, timeout=10)
        db = gpsdb.cursor()
        result = db.execute('select * from observations where posixtime > ?;', values)
        for item in result:
            returnarray.append(item)
        db.close()
    except sqlite3.OperationalError:
        print(f'Database select query FAILED - database locked')
    return returnarray


def db_data_get_all():
    returnarray = []
    try:
        gpsdb = sqlite3.connect(k.database, timeout=10)
        db = gpsdb.cursor()
        result = db.execute('select * from observations;')
        for item in result:
            returnarray.append(item)
        db.close()
    except sqlite3.OperationalError:
        print(f'Database get all FAILED - database locked')
    return returnarray