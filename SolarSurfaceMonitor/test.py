import numpy as np
import os
import glob
import time
import datetime
from calendar import timegm
import cv2
import mgr_mp4 as make_anim
import mgr_multicolour_diff as multidiff
import numpy as np

# file path seperator / or \ ???
pathsep = os.sep


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


files_blue = local_file_list_build('diffs_b')
files_blue = files_blue[-360:]
files_green = local_file_list_build('diffs_g')
files_green = files_green[-360:]
files_red = local_file_list_build('diffs_r')
files_red = files_red[-360:]

multifilelist = []
for file_b in files_blue:
    tmp = []
    tmp.append(file_b)
    b = file_b.split(pathsep)
    start_b = b[1]

    for file_g in files_green:
        g = file_g.split(pathsep)
        start_g = g[1]
        if start_g == start_b:
            tmp.append(file_g)

    for file_r in files_red:
        r = file_r.split(pathsep)
        start_r = r[1]
        if start_r == start_b:
            tmp.append(file_r)
    if len(tmp) == 3:
        multifilelist.append(tmp)

multidiff.wrapper(multifilelist, 'combined_diffs')