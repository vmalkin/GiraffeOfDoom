# THis will generate a simple line plot of solar wind speed for the last 3 carrington rotations
# and highlight repeating events.

import common_data as k
import sqlite3
import time

def db_getdata(starttime):
    item = [starttime]
    db = sqlite3.connect(k.database)
    cursor = db.cursor()
    cursor.execute("select * from sw_data where sw_data.sw_time > ?", item)
    for item in cursor.fetchall():
        print(item)

def wrapper():
    # start date is 100 days ago
    starttime = time.time() - (60 * 60 * 24 * 100)
    db_getdata(starttime)

