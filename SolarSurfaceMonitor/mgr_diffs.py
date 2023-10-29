import numpy as np
import os
import glob
import time
import datetime
from calendar import timegm

pathsep = os.sep

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
    imagelist = {}

    # get the file listing from the first key in the dictionary. we only want files in a particular date range
    for key in suvi_dictionary:
        filelist = local_file_list_build(suvi_dictionary[key]['store'])
        for pathname in filelist:
            p = pathname.split('_g16_s')
            pp = p[1].split('Z_e')
            pdate = utc2posix(pp[0], '%Y%m%dT%H%M%S')
            if pdate >= starttime:
               imagelist[pdate] = []

    for key in suvi_dictionary:
        filelist = local_file_list_build(suvi_dictionary[key]['store'])
        for pathname in filelist:
            p = pathname.split('_g16_s')
            pp = p[1].split('Z_e')
            pdate = utc2posix(pp[0], '%Y%m%dT%H%M%S')
            imagelist[pdate].append(pathname)

    for item in imagelist:
        print(imagelist[item])
