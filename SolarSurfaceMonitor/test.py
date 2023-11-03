import numpy as np
import os
import glob
import time
import datetime
from calendar import timegm
import cv2
import mgr_mp4 as make_anim

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



folder = 'diffs_g'
img_files = local_file_list_build(folder)
# a day is roughly 100 images
img_files = img_files[-360:]
make_anim.wrapper(img_files, 'diffs_191A')