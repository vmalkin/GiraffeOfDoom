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
    # We want the COUNT of S4 events for the hour over 40% AND less that 100
    s4_counter = 0
    for item in result:
        if item[1] > s4_altitude:
            if item[2] > s4_threshold:
                if item[2] <= 100:
                    s4_counter = s4_counter + 1
    db.close()
    return s4_counter


def wrapper(stats_dict):
    if os.path.isfile(k.file_means) is True:
        m = stats_dict["medianvalue"]
        s = stats_dict["mediansigma"]
        count_events = database_parse()

        result = "none"
        if count_events > (m + 2 * s):
            result = "low"

        if count_events > (m + 4 * s):
            result = "med"

        if count_events > (m + 6 * s):
            result = "high"

        nowtime = int(time.time())
        i = {"posixtime" : nowtime, "ionstate" : result}
        print(i)

        filepath = "ion.json"
        with open(filepath, "w") as j:
            json.dump(i, j)
