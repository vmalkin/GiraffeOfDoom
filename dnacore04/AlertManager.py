import sqlite3
import constants as k
import logging
import time
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
db = dna_core.cursor()
timeformat = '%Y-%m-%d %H:%M:%S'

def get_data():
    t = int(time.time() - (60*60*24))

    result = db.execute("select * from events;")
    # result = db.execute("select max(posix_time), station_id, message from events where posix_time > ? group by station_id;", [t])
    query_result = result.fetchall()
    db.close()
    return query_result

print(get_data())