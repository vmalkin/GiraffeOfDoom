import cv2
import os
import glob
import datetime
import calendar


def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    # return only a single channel
    greyimg = cv2.split(greyimg)
    greyimg = greyimg[0]
    return greyimg


def image_load(file_name):
    # Return a None if the image is currupt
    try:
        img = cv2.imread(file_name)
    except Exception as e:
        print(e)
        img = None
    return img


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


def wrapper(lasco_folder):
    time_threshold = 60 * 60 * 12
    # get image list of LASCO files for the last x-hours.
    dirlisting = get_dirlisting(lasco_folder)
    print(dirlisting)

    # if time difference between img_x, ing_y < time threshold
    for i in range(1, len(dirlisting)):
        if filename_converter(dirlisting[i]) - filename_converter(dirlisting[i - 1]) < time_threshold:
            # Convert img_x, img_y to greyscale
            img_x = image_load(dirlisting[i - 1])
            img_y = image_load(dirlisting[i])
            # Convert img_x, img_y to single channel
            img_x = greyscale_img(img_x)
            img_y = greyscale_img(img_y)

        #   New savefile = img_y name

    #   for img_x, img_y:
    #       for same pixel location in img_x, img_y:
    #           if diff between px_img_x and px_img_y greater than pixel_threshold:
    #               new_pixel = median pixel value
    #               else new_pixel = old_pixel
    #       save new image, img_z

    # CReate embossed effect image


wrapper("lasco_store_512")