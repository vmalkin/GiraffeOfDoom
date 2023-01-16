import cv2
import os
import glob
import datetime
import calendar
import numpy as np
import math
import time
from PIL import Image

def add_stamp(banner_text, image_object, filename):
    tt = time.time()
    tt = posix2utc(tt, "%Y-%m-%d %H:%M")
    cv2. rectangle(image_object, (0, 449), (511, 511), (255, 255, 255), -1)
    cv2.rectangle(image_object, (0, 0), (511, 20), (255, 255, 255), -1)
    colour = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.5
    font_color = colour
    font_thickness = 1
    banner = banner_text
    x, y = 5, 15
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    banner = 'LASCO coronagraph. Updated ' + tt + " UTC."
    x, y = 5, 466
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    font_size = 0.4
    font_color = colour
    font_thickness = 1

    banner = filename
    x, y = 5, 483
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'Courtesy of SOHO/LASCO consortium. SOHO is a project of'
    x, y = 5, 496
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'international cooperation between ESA and NASA'
    x, y = 5, 508
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


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


def colourise(final):
    new_image = cv2.applyColorMap(final, cv2.COLORMAP_BONE)
    return new_image


def wrapper(lasco_folder, enhanced_folder):
    print("*** Enhancer: Start")
    time_threshold = 60 * 60
    # get image list of LASCO files for the last x-hours.
    dirlisting = get_dirlisting(lasco_folder)
    dirlisting.sort()
    anim_enhanced = []
    anim_lasco = []

    # if time difference between img_x, ing_y < time threshold
    print("*** Enhancer: Removing partical hits from files")
    for i in range(1, len(dirlisting)):
        txt = "Denoising" + str(i) + " / " + str(len(dirlisting))
        print(txt)
        if filename_converter(dirlisting[i], "posix") - filename_converter(dirlisting[i - 1], "posix") < time_threshold:
            # load an automatically convert image to greyscale
            file_2 = lasco_folder + os.sep + dirlisting[i]
            file_1 = lasco_folder + os.sep + dirlisting[i - 1]
            img_2 = cv2.imread(file_1, 0)
            img_1 = cv2.imread(file_2, 0)

            cols = int(img_2.shape[0])
            rows = int(img_2.shape[1])

            threshold = 20
            denoised = np.full([cols, rows], 60, np.uint8)
            for a in range(0, rows):
                for b in range(0, cols):
                    x = int(img_2[a][b]) - int(img_1[a][b])
                    x = x * x
                    x = int(math.sqrt(x))
                    if x < threshold:
                        denoised[a][b] = img_2[a][b]

            picture = denoised
            # alpha value [1.0-3.0] CONTRAST
            # beta value [0-100] BRIGHTNESS
            alpha = 2.5
            beta = 80
            picture = cv2.convertScaleAbs(picture, alpha=alpha, beta=beta)

            # clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(10,10))
            # picture = clahe.apply(picture)

            # final = cv2.bitwise_not(final)
            final = colourise(picture)

            add_stamp("Processed at Dunedin Aurora", final, dirlisting[i])
            savefile = enhanced_folder + os.sep + dirlisting[i]
            cv2.imwrite(savefile, final)

            si = Image.open(savefile)
            stereoimage = Image.new("RGB", [cols, rows])
            stereoimage.paste(si)
            anim_enhanced.append(stereoimage)

    print("*** Enhancer: Saving GIF")
    anim_enhanced[0].save("cme.gif",
                        format="GIF",
                        save_all=True,
                        append_images=anim_enhanced[1:],
                        duration=50,
                        loop=0)
    print("*** Enhancer: Finished")