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
db = dna_core.cursor()
timeformat = '%Y-%m-%d %H:%M:%S'

def posix2utc(self, posixvalue):
    # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime(timeformat)
    return utctime

if __name__ == "__main__":
    finish_time = int(time.time())
    start_time = finish_time - (60*60*24)


    print("Closing database and exiting")
    dna_core.commit()
    db.close()
