import cv2
import time
import datetime
from calendar import timegm

import numpy as np


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time

def create_label(image, timestamp):
    # width, height, channels = image.shape
    width, height = image.shape
    label_height = int(height / 10)
    font_height = int(height / 12)
    cv2.rectangle(image, (0,0), (width,label_height), (0, 0, 0), -1)
    cv2.rectangle(image, (0, height - label_height), (width, height), (0, 0, 0), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    # colours are blue, green, red in opencv
    font_color = (255, 255, 255)
    font_thickness = 1
    label0 = "GOES SUVI 171A image processed at DunedinAurora.NZ Magnetic Observatory"
    label1 = "Image time: " + timestamp
    label2 = "Images courtesy of NOAA."
    cv2.putText(image, label0, (0, 50), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(image, label1, (0, 100), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(image, label2, (0, height - 80), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    return image

def image_read_fromfile(name):
    # Colour?
    # image = cv2.imread(name)

    # Greyscale?
    image = cv2.imread(name, 0)
    return image

def image_translate(imagename, translation_value):
    # translation_value is the number of rows (x and y)
    # we want to shift the image by.
    # Remove 2 rows/cols at end and add 2 rows/cols at beginning

    # width, height, channels = image.shape
    width, height = imagename.shape

    # delete columns axis = 1
    for i in range(0, translation_value):
        imagename = np.delete(imagename, [width - translation_value], axis=1)
    # delete rows axis = 0
    for i in range(0, translation_value):
        imagename = np.delete(imagename, [width - translation_value], axis=0)

    # insert columns
    for i in range(0, translation_value):
        # img_new = np.insert(img_new, 0, [0, 0, 0], axis=1)
        imagename = np.insert(imagename, 0, [0], axis=1)
    # insert rows
    for i in range(0, translation_value):
        imagename = np.insert(imagename, 0, imagename[0], axis=0)

    return imagename


def create_reticle(image):
    solar_diameter = 380
    width, height = image.shape
    x_offset = 0
    y_offset = 0
    x_centre = int(width / 2) + x_offset
    y_centre = int(height / 2) + y_offset
    cv2.circle(image, (x_centre, y_centre), solar_diameter, (0, 100, 0), 3)
    return image


def wrapper(filepathlist, diffstore, pathsep):
    print("*** Differencing started")
    for i in range(1, len(filepathlist)):
        old_name = filepathlist[i - 1]
        ot1 = old_name.split("_g18_s")
        ot2 = ot1[1].split("Z_e")
        old_time = utc2posix(ot2[0], "%Y%m%dT%H%M%S")

        new_name = filepathlist[i]
        nt1 = new_name.split("_g18_s")
        nt2 = nt1[1].split("Z_e")
        new_time = utc2posix(nt2[0], "%Y%m%dT%H%M%S")

        # large gaps im image times should NOT be diffrenced
        if (new_time - old_time) < (60 * 10):
            # https: // stackoverflow.com / questions / 58638506 / how - to - make - a - jpg - image - semi - transparent
            # Make image 50% transparent
            img_old = image_read_fromfile(old_name)
            # # invert one image
            img_old = cv2.bitwise_not(img_old)

            img_new = image_read_fromfile(new_name)
            img_new = image_translate(img_new, 1)

            # img_diff = cv2.absdiff(img_old, img_new)
            img_diff = cv2.addWeighted(img_old, 0.5, img_new, 0.5, 0)
            img_diff = cv2.medianBlur(img_diff, 3)

            clahe = cv2.createCLAHE(clipLimit=20, tileGridSize=(10, 10))
            img_diff = clahe.apply(img_diff)

            # Add watermark to image
            timestamp = posix2utc(new_time, "%Y-%m-%d %H:%M UTC")
            img_diff = create_label(img_diff, timestamp)
            img_diff = create_reticle(img_diff)

            # Give the file the UTC time of the start of the observation
            diff_filename = diffstore + pathsep + ot2[0] + "_df.png"
            cv2.imwrite(diff_filename, img_diff)
    print("*** Differencing FINISHED")