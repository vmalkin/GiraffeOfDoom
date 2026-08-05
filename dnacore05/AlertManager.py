import sqlite3
import constants as k
import logging
import time
import datetime
"""
logging levels in order of least --> most severity:
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""
errorloglevel = logging.WARNING
logging.basicConfig(filename=k.error_log, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

dna_core = sqlite3.connect(k.dbfile)

timeformat = '%Y-%m-%d %H:%M'
# ascii_spacer = "__________________________________________________________________________________"
ascii_spacer = " "

def posix2utc(posixtime, timeformat):
    # timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def get_data():
    db = dna_core.cursor()
    t = int(time.time() - (60*60*24))

    # result = db.execute("SELECT * FROM sqlite_master")
    result = db.execute("select max(posix_time), station_id, message from events where posix_time > ? group by station_id;", [t])
    # result = db.execute("select posix_time, station_id, message from events")
    x = result.fetchall()
    db.close()
    return x

t = time.time()
t = posix2utc(t,timeformat)
print("Dunedin Aurora - Space weather status. Generated  " + t)
print(ascii_spacer)
d = get_data()
for item in d:
    eventtime = posix2utc(item[0], timeformat)
    event = item[2]
    print(eventtime + " " + event)
    print(ascii_spacer)


