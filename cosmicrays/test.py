import mgr_plot_flux
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
    result = cursor.execute("select posixtime from data where posixtime > ? order by posixtime asc", [starttime])
    for line in result:
        d = line[0]
        tempdata.append(d)
    db.close()
    return tempdata


data = database_get_data(24*7)
tt = int(time.time())
mgr_plot_flux.wrapper(data)
