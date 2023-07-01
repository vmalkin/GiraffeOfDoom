import os
import time
from datetime import datetime
from calendar import timegm
from PIL import Image

timeformat = "%Y%m%dT%H%M%S"
def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time

directory_seperator = os.sep
def wrapper(filelist):
    print("*** GIF creation started")
    nowtime = int(time.time())
    starttime = nowtime - 86400
    processinglist = []
    for filepath in filelist:
        ff = filepath.split(directory_seperator)
        fff = ff[1].split("_")
        filetime = utc2posix(fff[0], timeformat)
        if filetime >= starttime:
            processinglist.append(filepath)

    images = []
    for file in processinglist:
        im = Image.open(file)
        images.append(im)
    images[0].save("diffs_sun.gif", save_all=True, append_images=images[1:], duration=100, loop=0)
    print("*** GIF creation FINISHED")


