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
stations = ["Ruru_Obs", "GOES_16", "Geomag_Bz", "SW_speed", "SW_Density"]


def posix2utc(posixvalue):
    # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
    utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime(timeformat)
    return utctime


def save_logfiles():
    finish_time = int(time.time())
    start_time = finish_time - (60 * 60 * 24)

    # result = db.execute("select station_data.posix_time, station_data.data_value from station_data")
    # print(result.fetchall())
    for station in stations:
        result = db.execute("select station_data.posix_time, station_data.data_value from station_data "
                            "where station_data.station_id = ? and station_data.posix_time > ?", [station, start_time])

        current_stationdata = result.fetchall()

        # Setup for saving basic log files
        savefile = station + "_" + datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d') + ".csv"
        nowfile = station + ".csv"
        tempfile = []
        header = station + ", data"
        tempfile.append(header)

        for item in current_stationdata:
            date = posix2utc(item[0])
            data = item[1]
            dp = date + "," + data
            tempfile.append(dp)

        with open(savefile, "w") as s:
            for item in tempfile:
                s.write(item + "\n")
        s.close()

        with open(nowfile, "w") as n:
            for item in tempfile:
                n.write(item + "\n")
        n.close()


if __name__ == "__main__":
    save_logfiles()

    print("Closing database and exiting")
    dna_core.commit()
    db.close()
