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
    width, height, channels = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    # colours are blue, green, red in opencv
    font_color = (255, 255, 255)
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
            # https: // stackoverflow.com / questions / 58638506 / how - to - make - a - jpg - image - semi - transparent
            # Make image 50% transparent
            img_old = cv2.imread(old_name)
            # img_old = cv2.cvtColor(img_old, cv2.COLOR_BGR2BGRA)
            # # Set alpha layer semi-transparent with Numpy indexing, B=0, G=1, R=2, A=3
            # img_old[..., 3] = 255

            img_new = cv2.imread(new_name)
            # invert one image
            img_new = cv2.bitwise_not(img_new)
            # img_new = cv2.cvtColor(img_new, cv2.COLOR_BGR2BGRA)
            # # Set alpha layer semi-transparent with Numpy indexing, B=0, G=1, R=2, A=3
            # img_new[..., 3] = 255


            divisor = np.full_like(img_old, 2)
            img_old = np.floor_divide(img_old, divisor)
            img_new = np.floor_divide(img_new, divisor)

            img_diff = cv2.addWeighted(img_old, 0.5, img_new, 0.5, 0)
            # img_diff = np.add(img_old, img_new)

            # lab = cv2.cvtColor(img_diff, cv2.COLOR_BGR2LAB)
            # l_channel, a, b = cv2.split(lab)
            # # Applying CLAHE to L-channel
            # # feel free to try different values for the limit and grid size:
            # clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(8, 8))
            # cl = clahe.apply(l_channel)
            # # merge the CLAHE enhanced L-channel with the a and b channel
            # limg = cv2.merge((cl, a, b))
            #
            # # Converting image from LAB Color model to BGR color spcae
            # img_diff = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


            timestamp = posix2utc(new_time, "%Y-%m-%d %H:%M UTC")
            img_diff = create_label(img_diff, timestamp)

            # Give the file the UTC time of the start of the observation
            diff_filename = diffstore + pathsep + ot2[0] + "_df.png"
            # old = diffstore + pathsep + ot2[0] + "_o_df.png"
            # new = diffstore + pathsep + ot2[0] + "_n_df.png"
            cv2.imwrite(diff_filename, img_diff)
            # cv2.imwrite(old, img_old)
            # cv2.imwrite(new, img_new)
