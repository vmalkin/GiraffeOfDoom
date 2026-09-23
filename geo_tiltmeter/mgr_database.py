import sqlite3
import constants as k
import os


def db_create():
    # create database!
    database = sqlite3.connect(k.database)
    cursor = database.cursor()
    database.execute("PRAGMA journal_mode=WAL;")
    cursor.execute('drop table if exists observations;')
    cursor.execute('create table observations ('
               'posixtime real,'
               'tiltdata real'
               ');')
    database.commit()
    cursor.close()
    # This might be needed to ensure we have permissions to write to the DB. Linux of course
    os.chmod(k.database, 0o664)


def db_data_add(insertdata):
    try:
        with sqlite3.connect(k.database, timeout=10) as database:
            cursor = database.cursor()
            cursor.executemany(
                'insert into observations(posixtime, tiltdata) '
                           'values (?, ?);',
                insertdata
            )
            # The with sqlite3.connect(...) context manager automatically commits
            # if the block exits successfully, and rolls back if an exception occurs.
            # We MUST however close the cursor object
            # database.commit()
            cursor.close()

    except sqlite3.OperationalError as e:
        print(f'Database INSERT FAILED: {e}')


def db_data_get(timestart, timeend):
    try:
        with sqlite3.connect(k.database, timeout=10) as database:
            cursor = database.cursor()
            result = cursor.execute(
                'select * from observations where posixtime between ? and ? order by posixtime;',
                (timestart, timeend)
            ).fetchall()
            cursor.close()
        return result

    except sqlite3.OperationalError as e:
        print(f'Database SELECT FAILED: {e}')
        return None


def db_data_all():
    try:
        with sqlite3.connect(k.database, timeout=10) as database:
            cursor = database.cursor()
            result = cursor.execute(
                'select * from observations order by posixtime;'
            ).fetchall()
            cursor.close()
        return result

    except sqlite3.OperationalError as e:
        print(f'Database SELECT ALL FAILED: {e}')
        return None