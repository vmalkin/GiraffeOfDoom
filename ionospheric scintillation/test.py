import sqlite3
import time
import qpr_24hr_cumulative

sat_database = "gps_satellites.db"
# readings below this altitude for satellites may be distorted due to multi-modal reflection
optimum_altitude = 25

def database_parse(hourduration):
    starttime = int(time.time()) - (60 * 60 * hourduration)
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select sat_id, posixtime, alt, az, s4, snr from satdata where posixtime > ? and alt > ? order by posixtime asc', [starttime, optimum_altitude])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4], item[5])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


if __name__ == "__main__":
    querydata_48 = database_parse(48)
    qpr_24hr_cumulative.wrapper(querydata_48)