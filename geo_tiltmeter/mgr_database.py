import sqlite3
import constants as k


def db_create():
    # create database!
    gpsdb = sqlite3.connect(k.database)
    db = gpsdb.cursor()
    gpsdb.execute("PRAGMA journal_mode=WAL;")
    db.execute('drop table if exists observations;')
    db.execute('create table observations ('
               'posixtime real,'
               'tiltdata real'
               ');')
    gpsdb.commit()
    db.close()


def db_data_add(insertdata):
    try:
        with sqlite3.connect(k.database, timeout=10) as database:
            db = database.cursor()
            db.executemany(
                'insert into observations(posixtime, tiltdata) '
                           'values (?, ?);',
                insertdata
            )
            # The with sqlite3.connect(...) context manager automatically commits
            # if the block exits successfully, and rolls back if an exception occurs.
            # database.commit()

    except sqlite3.OperationalError as e:
        print(f'Database data insert FAILED: {e}')


def db_data_get(timestart, timeend):
    try:
        with sqlite3.connect(k.database, timeout=10) as database:
            db = database.cursor()
            result = db.execute(
                'select * from observations where posixtime between ? and ? order by posixtime;',
                (timestart, timeend)
            ).fetchall()
        return result

    except sqlite3.OperationalError as e:
        print(f'Database data SELECT FAILED: {e}')
        return None

