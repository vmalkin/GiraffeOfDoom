import mgr_plotter
import sqlite3
import time
import datetime

database = "events.db"

def database_get_data(hours_duration):
    duration = hours_duration * 3600
    tempdata = []
    starttime = int(time.time()) - duration
    db = sqlite3.connect(database)
    cursor = db.cursor()
    result = cursor.execute("select * from data where data.posixtime > ? order by data.posixtime asc", [starttime])
    for line in result:
        dt = line[0]
        da = line[1]
        d = [dt, da]
        tempdata.append(d)
    db.close()
    return tempdata


data = database_get_data(48)
mgr_plotter.wrapper(data)