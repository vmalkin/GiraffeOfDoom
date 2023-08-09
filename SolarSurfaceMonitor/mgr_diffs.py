import numpy as np
import os
import glob
import time
import datetime
from calendar import timegm

pathsep = os.sep


class ImageMaster:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.path_red = None
        self.path_green = None
        self.path_blue = None


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


def local_file_list_build(directory):
    # Builds and returns a list of files contained in the directory.
    # List is sorted into A --> Z order
    dirlisting = []
    path = directory + pathsep + "*.*"
    for name in glob.glob(path):
        name = os.path.normpath(name)
        # seperator = os.path.sep
        # n = name.split(seperator)
        # nn = n[1]
        dirlisting.append(name)
    dirlisting.sort()
    return dirlisting


def wrapper(suvi_dictionary):
    starttime = int(time.time()) - 86400
    # Start with an empty image list
    imagelist = []



    # get the file listing from the first key in the dictionary. we only want files in a particular date range
    for key in suvi_dictionary:
        t = []
        filelist = local_file_list_build(suvi_dictionary[key]['store'])
        for pathname in filelist:
            p = pathname.split('_g16_s')
            pp = p[1].split('Z_e')
            pdate = utc2posix(pp[0], '%Y%m%dT%H%M%S')
            if pdate >= starttime:
                pass




    # THe files all have the same datetime component in the name. if this name does not exist in the image list
    #  create a new image
    # add the filepath to the correct imagelist variable.
    # Else add the filepath to the exiting image list variable.
    # At the end of this, we should have a populated image list with path variables populated.
