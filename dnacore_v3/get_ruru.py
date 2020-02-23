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
    return(int(time.mktime(dt)))
    # print(time.time())


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
            try:
                r = row.split(',')
                posix_dt = utc2posix(r[0])
                value = round(float(r[1]), 3)
                dp = str(posix_dt) + "," + str(value)
                templist.append(dp)
            except IndexError:
                logging.error("ERROR: list index out of range")
    else:
        logging.error("ERROR: Could not get data from URL")

    print(templist)

    for row in templist:
        row = row.split(",")
        print('insert into station_data(station_id, posix_time, data_value) values ("ruru_obs", {0}, {1});'.format(row[0], row[1]))

    if len(templist) > 0:
        # for row in templist:
        pass
        # get latest datetime for the observatory from database, if none, just append current data
        # from data, only keep values younger than most recent datetime from database
        # append data to database
    else:
        logging.error("ERROR: No data after parsing datetimes")

    print("Closing database and exiting")
    dna_core.commit()
    db.close()