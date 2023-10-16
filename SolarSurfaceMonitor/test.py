import glob
import requests
import os
import time
import mgr_diffs as diffs
import mgr_gif as make_gif

pathsep = os.sep
suvidata = {
    '171': {
        'store': 'store_b',
        'diffs': 'diffs_b',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/'
    },
    '195': {
        'store': 'store_g',
        'diffs': 'diffs_g',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/'
    },
    '284': {
        'store': 'store_r',
        'diffs': 'diffs_r',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/'
    }
}

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

diffs.wrapper(suvidata)
