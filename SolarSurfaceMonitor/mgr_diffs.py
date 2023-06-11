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
        new_name = filepathlist[i]

        img_old = cv2.imread(old_name, cv2.IMREAD_GRAYSCALE)
        img_new = cv2.imread(new_name, cv2.IMREAD_GRAYSCALE)

        img_diff = img_new - img_old

        diff_filename = diffstore + pathsep +  str(i) + "_df.jpg"
        cv2.imwrite(diff_filename, img_diff)
