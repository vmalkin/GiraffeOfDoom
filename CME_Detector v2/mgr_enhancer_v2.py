import cv2
import os
import glob
import datetime
import calendar
import numpy as np
import math


def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    # return only a single channel
    greyimg = cv2.split(greyimg)
    greyimg = greyimg[0]
    return greyimg


# def image_load(file_name):
#     # Return a None if the image is currupt
#     try:
#         img = cv2.imread(file_name)
#     except Exception as e:
#         print(e)
#         img = None
#     return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def get_dirlisting(folder):
    dirlisting = []
    path = os.path.join(folder, "*.jpg")
    for name in glob.glob(path):
        name = os.path.normpath(name)
        seperator = os.path.sep
        n = name.split(seperator)
        nn = n[1]
        dirlisting.append(nn)
        # make sure they are in chronological order by name
    dirlisting.sort()
    return dirlisting


def filename_converter(filename, switch="posix"):
    # Name has format 20221230_2342_c3_512.jpg
    f = filename.split("_")
    yyyymmdd = f[0]
    hhmm = f[1]
    year = (yyyymmdd[:4])
    month = (yyyymmdd[4:6])
    day = (yyyymmdd[6:])
    hour = (hhmm[:2])
    min = (hhmm[2:])
    utc_string = year + '-' + month + '-' + day + ' ' + hour + ':' + min
    filename = year + '-' + month + '-' + day + '-' + hour + '-' + min + ".jpg"
    # utc time string
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')

    if switch == "utc":
        # utc time string
        returnstring = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')
    elif switch == "filename":
        returnstring = filename
    else:
        returnstring = calendar.timegm(dt.timetuple())
    # return posix by default
    return returnstring


def wrapper(lasco_folder, enhanced_folder):
    time_threshold = 60 * 60
    # get image list of LASCO files for the last x-hours.
    dirlisting = get_dirlisting(lasco_folder)
    dirlisting.sort()

    # if time difference between img_x, ing_y < time threshold
    for i in range(1, len(dirlisting)):
        if filename_converter(dirlisting[i], "posix") - filename_converter(dirlisting[i - 1], "posix") < time_threshold:
            # load an automatically convert image to greyscale
            file_2 = dirlisting + os.sep + dirlisting[i]
            file_1 = dirlisting + os.sep + dirlisting[i - 1]
            img_2 = cv2.imread(file_1, 0)
            img_1 = cv2.imread(file_2, 0)

            cols = int(img_2.shape[0])
            rows = int(img_2.shape[1])

            threshold = 20
            denoised = np.full([cols, rows], 60, np.uint8)
            for i in range(0, rows):
                for j in range(0, cols):
                    x = int(img_2[i][j]) - int(img_1[i][j])
                    x = x * x
                    x = int(math.sqrt(x))
                    if x < threshold:
                        denoised[i][j] = img_2[i][j]

                    picture = cv2.GaussianBlur(denoised, (3,3), 0)
                    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(10,10))
                    final = clahe.apply(picture)
                    # final1 = cv2.bitwise_not(final1)
