import cv2
import time
import datetime
from calendar import timegm


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time


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

            img_diff = cv2.absdiff(img_new, img_old)
            img_diff = cv2.equalizeHist(img_diff)
            # img_diff = cv2.erode(img_diff, (10,10))
            # img_diff = cv2.dilate(img_diff, (20, 20))
            # # 0 and 1 or over
            # contrast = 0
            # # -127 to 127
            # brightness = 20
            # img_diff = cv2.convertScaleAbs(img_diff, contrast, brightness)
            # img_diff = cv2.bilateralFilter(img_diff, 5, 13, 13)

            # Give the file the UTC time of the start of the observation
            diff_filename = diffstore + pathsep + ot2[0] + "_df.jpg"
            cv2.imwrite(diff_filename, img_diff)
