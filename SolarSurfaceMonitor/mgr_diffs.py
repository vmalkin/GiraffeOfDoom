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

def create_label(image, text):
    width, height = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    font_color = (255, 150, 0)
    font_thickness = 1
    cv2.putText(image, text, (100, height - 100), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    return image



def wrapper(filepathlist, diffstore, pathsep):
    for i in range(1, len(filepathlist)):
        old_name = filepathlist[i - 1]
        ot1 = old_name.split("_g18_s")
        ot2 = ot1[1].split("Z_e")
        old_time = utc2posix(ot2[0], "%Y%m%dT%H%M%S")

        new_name = filepathlist[i]
        nt1 = new_name.split("_g18_s")
        nt2 = nt1[1].split("Z_e")
        new_time = utc2posix(nt2[0], "%Y%m%dT%H%M%S")

        if (new_time - old_time) < 86400:
            img_old = cv2.imread(old_name, cv2.IMREAD_GRAYSCALE)
            img_new = cv2.imread(new_name, cv2.IMREAD_GRAYSCALE)

            img_old = np.float32(img_old)
            img_new = np.float32(img_new)

            img_diff = img_new - img_old

            # alpha is the contrast value. To lower the contrast, use 0 < alpha < 1. And for higher contrast use alpha > 1.
            # beta is the brightness value. A good range for brightness value is [-127, 127]
            alpha = 1
            beta = 20
            img_diff = cv2.convertScaleAbs(img_diff, alpha, beta)
            # # img_diff = cv2.erode(img_diff, (5,5))
            # # img_diff = cv2.medianBlur(img_diff, 3)
            # # img_diff = cv2.bilateralFilter(img_diff, 5, 13, 13)

            timestamp = posix2utc(new_time, "%Y-%m-%d %H:%M UTC")
            img_diff = create_label(img_diff, timestamp)

            # Give the file the UTC time of the start of the observation
            diff_filename = diffstore + pathsep + ot2[0] + "_df.jpg"
            cv2.imwrite(diff_filename, img_diff)
