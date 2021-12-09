from datetime import datetime
import time
dt_format = "%Y-%m-%d %H:%M:%S"

def posix_to_utc(posixtime):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(dt_format)
    return utctime

now = time.time()

print(posix_to_utc(now))