import sqlite3
import constants as k


def db_create():
    # create database!
    gpsdb = sqlite3.connect(k.database)
    db = gpsdb.cursor()

    db.execute('drop table if exists observations;')

    db.execute('create table observations ('
               'posixtime real,'
               'tiltdata real'
               ');')
    gpsdb.commit()
    db.close()


def db_data_add(insertdata):
    # this method expects an array with each element in the array being:
    # [1737274820, '21.05', '99740.46'] (posixtime, temperature, pressure)
    try:
        gpsdb = sqlite3.connect(k.database, timeout=10)
        db = gpsdb.cursor()
        for item in insertdata:
            posixtime = item[0]
            tiltdata = item[1]
            values = [posixtime, tiltdata]
            db.execute('insert into observations(posixtime, tiltdata) '
                       'values (?, ?);', values)
        gpsdb.commit()
        db.close()
    except sqlite3.OperationalError:
        print(f'Database data insert FAILED - database locked')


def db_data_get(timestart, timeend):
    returnarray = []
    values = [timestart, timeend]
    try:
        gpsdb = sqlite3.connect(k.database, timeout=10)
        db = gpsdb.cursor()
        # result = db.execute('select * from observations where posixtime > ?;', values)
        result = db.execute('select * from observations where posixtime between ? and ? order by posixtime;', values)
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
        result = db.execute('select posixtime, tiltdata from observations order by posixtime;')
        for item in result:
            returnarray.append(item)
        db.close()
    except sqlite3.OperationalError:
        print(f'Database get all FAILED - database locked')
    return returnarray