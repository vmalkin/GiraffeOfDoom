from standard_stuff import posix2utc
from time import time
import os

def getposixtime():
    timevalue = int(time())
    return timevalue



def wrapper(data, logfile_directory):
    # Current data is CSV file with format "posixtime, datavalue"
    currentdata = data
    tmp = []
    filename = posix2utc(time(), '%Y-%m-%d') + ".csv"
    savefile_name = logfile_directory + os.sep +  filename

    with open(savefile_name, "w") as s:
        s.write("Datetime UTC, Datavalue Arbitrary Units\n")
        for item in currentdata:
            dt = posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
            da = str(item[1])
            dp = dt + "," + da + "\n"
            s.write(dp)
    s.close()
    print("*** Daily Logfile: Saved " + savefile_name)
