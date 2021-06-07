import pickle
import time
import constants as k
import os
from statistics import median, mean
import sqlite3
import json

sat_database = "gps_satellites.db"
s4_altitude = 40
s4_threshold = 40

def load_values(pickle_file):
    returnlist = []
    if os.path.exists(pickle_file) is True:
        try:
            returnlist = pickle.load(open(pickle_file, "rb"))
        except EOFError:
            print("Pickle file is empty")
    print("Loaded pickle file is " + str(len(returnlist)) + " records long")
    return returnlist


def database_parse():
    starttime = int(time.time()) - (60 * 60 * 24)
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select posixtime, alt, s4 from satdata where posixtime > ? and alt > ? order by posixtime asc', [starttime, s4_altitude])
    # We want the COUNT of S4 events for the hour over 40%
    s4array = []
    for item in result:
        if item[1] > s4_altitude:
            if item[2] > s4_threshold and item[2] <= 100:
                s4array.append(item[2])
    db.close()
    return s4array


def wrapper(stats_dict):
    if os.path.isfile(k.statsfile_mean) is True:
        m = stats_dict["medianvalue"]
        s = stats_dict["mediansigma"]
        queryresult = database_parse()
        q = mean(queryresult)
        print("Values for JSON, Result, Median, Sigma ", q, m, s)

        result = "none"
        if q > (m + 2 * s):
            result = "low"

        if q > (m + 4 * s):
            result = "med"

        if q > (m + 6 * s):
            result = "high"

        nowtime = int(time.time())
        i = {"posixtime" : nowtime, "ionstate" : result}
        print(i)

        filepath = "ion.json"
        with open(filepath, "w") as j:
            json.dump(i, j)
