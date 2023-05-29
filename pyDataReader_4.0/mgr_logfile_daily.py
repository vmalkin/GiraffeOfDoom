from standard_stuff import posix2utc
import sqlite3
from time import time
import os

def getposixtime():
    timevalue = int(time())
    return timevalue


def database_get_data(dba):
    tempdata = []
    starttime = getposixtime() - 86400
    db = sqlite3.connect(dba)
    try:
        cursor = db.cursor()
        result = cursor.execute("select * from data where data.posixtime > ? order by data.posixtime asc", [starttime])
        for line in result:
            dt = line[0]
            da = line[1]
            d = [dt, da]
            tempdata.append(d)

    except sqlite3.OperationalError:
        print("Database is locked, try again!")
    db.close()
    return tempdata


def wrapper(database, logfile_directory):
    # Current data is CSV file with format "posixtime, datavalue"
    currentdata = database_get_data(database)
    tmp = []
    filename = posix2utc(time(), '%Y-%m-%d') + ".csv"
    savefile_name = logfile_directory + os.sep +  filename

    with open(savefile_name, "w") as s:
        s.write("Datetime UTC, Datavalue Arbitrary Units\n")
        for item in currentdata:
            dt = posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
            da = str(item[1])
            dp = dt + "," + da + "\n"
            s.write(dp)
    s.close()
    print("*** Daily Logfile: Saved " + savefile_name)
