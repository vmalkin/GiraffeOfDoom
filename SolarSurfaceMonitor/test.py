import numpy as np
import os
import glob
import time
import datetime
from calendar import timegm
import cv2
import mgr_mp4 as make_anim
import mgr_multicolour_v2 as multicolour

# file path seperator / or \ ???
pathsep = os.sep
#
# def local_file_list_build(directory):
#     # Builds and returns a list of files contained in the directory.
#     # List is sorted into A --> Z order
#     dirlisting = []
#     path = directory + pathsep + "*.*"
#     for name in glob.glob(path):
#         name = os.path.normpath(name)
#         # seperator = os.path.sep
#         # n = name.split(seperator)
#         # nn = n[1]
#         dirlisting.append(name)
#     dirlisting.sort()
#     return dirlisting
#
#
#
# folder = 'diffs_g'
# img_files = local_file_list_build(folder)
# # a day is roughly 100 images
# img_files = img_files[-360:]
# make_anim.wrapper(img_files, 'diffs_195A')
#
# folder = 'diffs_b'
# img_files = local_file_list_build(folder)
# # a day is roughly 100 images
# img_files = img_files[-360:]
# make_anim.wrapper(img_files, 'diffs_171A')
#
# folder = 'diffs_r'
# img_files = local_file_list_build(folder)
# # a day is roughly 100 images
# img_files = img_files[-360:]
# make_anim.wrapper(img_files, 'diffs_284A')

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



pathlist = []
for key in suvidata:
    pathlist.append(suvidata[key]['diffs'])

img_tmp = []
for pathname in pathlist:
    filenames = local_file_list_build(pathname)
    filenames = filenames[-360:]
    img_tmp.append(filenames)

images_parsed = []
for i in range(0, len(img_tmp[0])):
    tmp = []
    for j in range(0, len(img_tmp)):
        tmp.append(img_tmp[j][i])
    images_parsed.append(tmp)

# image list is in format [[r1, g1, b1], [r2, g2, b2]...]
multicolour.wrapper(images_parsed, 'test')

folder = 'test'
img_files = local_file_list_build(folder)
# a day is roughly 100 images
img_files = img_files[-360:]
make_anim.wrapper(img_files, 'test_diffs')