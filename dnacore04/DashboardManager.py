import sqlite3
import constants as k
import logging
import time
import datetime
import json
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

dataforjson = {
"utc" : "0000-00-00 00:00",
"speed" : "none",
"density" : "none",
"mag" : "none",
"ion" : "none",
"dna" : "none",
"bz" : "none"
}

timeformat = '%Y-%m-%d %H:%M'
# ascii_spacer = "__________________________________________________________________________________"
ascii_spacer = " "

def posix2utc(posixtime, timeformat):
    # timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def get_data():
    db = dna_core.cursor()
    t = int(time.time() - (60*20))

    # result = db.execute("SELECT * FROM sqlite_master")
    result = db.execute("select max(posix_time), station_id, message from dashboard where posix_time > ? group by station_id;", [t])
    # result = db.execute("select * from dashboard")
    x = result.fetchall()
    db.close()
    return x

t = time.time()
t = posix2utc(t,timeformat)
print("Dunedin Aurora - Space weather status. Generated  " + t)
print(ascii_spacer)

d = get_data()
t = int(time.time())
utc = posix2utc(t, timeformat)
for item in d:
    if item[1] == "GOES_16":
        dataforjson["mag"] = item[2]

    if item[1] == "Geomag_Bz":
        dataforjson["bz"] = item[2][:-1]

    if item[1] == "Ruru_Obs":
        dataforjson["dna"] = item[2]

    if item[1] == "SW_Density":
        dataforjson["density"] = item[2]

    if item[1] == "SW_speed":
        dataforjson["speed"] = item[2]

dataforjson["utc"] = utc + " UTC"

print(dataforjson)
filepath = "data.json"
with open(filepath, "w") as j:
    json.dump(dataforjson, j)
