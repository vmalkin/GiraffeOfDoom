import numpy as np
import os
import glob
import time
import datetime
from calendar import timegm
import cv2

pathsep = os.sep


def create_label(image, timestamp):
    # width, height, channels = image.shape
    width, height, depth = image.shape
    label_height = int(height / 10)
    font_height = int(height / 12)
    cv2.rectangle(image, (0,0), (width,label_height), (0, 0, 0), -1)
    cv2.rectangle(image, (0, height - label_height), (width, height), (0, 0, 0), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    # colours are blue, green, red in opencv
    font_color = (255, 255, 255)
    font_thickness = 1
    label0 = "GOES SUVI 171A, 195A, 284A multispectral image."
    label1 = "Image time: " + timestamp
    label2 = "Images courtesy of NOAA. Processed at DunedinAurora.NZ"
    cv2.putText(image, label0, (0, 50), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(image, label1, (0, 100), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(image, label2, (0, height - 80), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    return image


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


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


def wrapper(pathlist, save_folder):
    print('*** BEGIN multicolour processing ', save_folder)

    if os.path.exists(save_folder) is False:
        os.makedirs(save_folder)

    for i in range(0, len(pathlist)):
        files = pathlist[i]
        # print(files)
        if len(files) == 3:
            b = cv2.imread(files[0], 0)
            r = cv2.imread(files[1], 0)
            g = cv2.imread(files[2], 0)

            filename = str(i) + ".png"

            colour_img = cv2.merge([b, g, r])
            # colour_img = cv2.merge([g, r, b])

            # create_label(colour_img, pp[0])
            fc = save_folder + pathsep + str(filename)
            cv2.imwrite(fc, colour_img)

    print('*** END multicolour processing')
