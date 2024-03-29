import os
import time
from datetime import datetime
from calendar import timegm
from PIL import Image

timeformat = "s%Y%m%dT%H%M%SZ"


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


directory_separator = os.sep
def wrapper(filelist, label):
    print("*** GIF creation started for ", label)
    # nowtime = int(time.time())
    # starttime = nowtime - 86400
    # processinglist = []
    # for filepath in filelist:
    #     ff = filepath.split(directory_separator)
    #     fff = ff[1].split("_")
    #     filetime = utc2posix(fff[3], timeformat)
    #     # if filetime >= starttime:
    #     processinglist.append(filepath)

    images = []
    for file in filelist:
        try:
            im = Image.open(file)
            im = im.resize((640, 640))
            images.append(im)
        except:
            print('!!! Unable to open image for GIF creation, skipping')
    filename = "gif_" + label + ".gif"
    images[0].save(filename, save_all=True, append_images=images[1:], duration=100, loop=0)
    print("*** GIF creation FINISHED")


