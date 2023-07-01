import glob
import requests
import os
import time
import mgr_diffs_2 as diffs
import mgr_gif as make_gif

pathsep = os.sep
diffs_store = "difference_images"

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


diff_files = local_file_list_build(diffs_store)
make_gif.wrapper(diff_files)