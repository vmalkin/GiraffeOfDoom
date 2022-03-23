import mgr_s4_tracker_v1
import mgr_s4_count


import sqlite3
import time

# This is the query output that will be used to generate graphs and plots etc.
querydata_24 = []
querydata_48 = []
current_stats = []
sat_database = "gps_satellites.db"
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

interval = 24 * 10
querydata = database_parse(interval)

timeformat = '%Y-%m-%d %H:%M:%S'
sat_database = "gps_satellites.db"
integration_time = 30
optimum_altitude = 25

print("***************************** Start Query Processor")
# mgr_polar_noise_tracks.wrapper(querydata_24)
mgr_s4_tracker_v1.wrapper(interval)
mgr_s4_count.wrapper()







