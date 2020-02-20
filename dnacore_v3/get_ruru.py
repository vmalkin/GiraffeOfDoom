import sqlite3
import constants as k
import logging
import requests
import datetime, time

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
datasource = "http://www.ruruobservatory.org.nz/dr01_1hr.csv"


def posix2utc(self, posixvalue):
    # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    return utctime


def utc2posix(utc_string):
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S').utctimetuple()
    print(time.mktime(dt))


if __name__ == "__main__":
    # connect if necessary
    # get data. If none, abort
    try:
        result = requests.get(datasource, timeout=20)
    except Exception:
        logging.error("Unable to get data from URL")

    if result.status_code == 200:
        # else parse for datetime, data
        result = result.content.decode('utf-8')
        webdata = result.split('\n')

        # the first line is just header data
        webdata.pop(0)

        # convert datetime to posix values
        templist = []
        for row in webdata:
            r = row.split(',')
            posix_dt = utc2posix(r[0])
            dp = posix_dt + "," + r[1]
            templist.append(dp)
    else:
        logging.error("ERROR: Could not get data from URL")

    if len(templist) > 0:
        # get latest datetime for the observatory from database, if none, just append current data
        try:
            db_result = db.execute('select * from station_data where station_id = "ruru_obs";')
            if len(db_result) == 0:
                for row in templist:
                    db.execute('insert into station_data(station_id, posix_time, data_value) values ("ruru_obs", ?, ?)', row[0], row[1])
        except Exception:
            logging.critical("CRITICAL ERROR: Cannot connect to database to get datetime value")
        # from data, only keep values younger than most recent datetime from database
        # append data to database
    else:
        logging.error("ERROR: No data after parsing datetimes")

    print("Closing database and exiting")
    dna_core.commit()
    db.close()