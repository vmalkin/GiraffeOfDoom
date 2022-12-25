from PIL import Image
import cv2
import datetime
import time
import calendar
import os
import glob


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


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


def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    return greyimg


def filehour_converter(yyyymmdd, hhmm):
    year = (yyyymmdd[:4])
    month = (yyyymmdd[4:6])
    day = (yyyymmdd[6:])
    hour = (hhmm[:2])
    min = (hhmm[2:])
    utc_string = year + '-' + month + '-' + day + ' ' + hour + ':' + min
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')
    ts = calendar.timegm(dt.timetuple())
    return ts


def image_load(file_name):
    # Return a None if the image is currupt
    try:
        pil_image = Image.open(file_name)
        # pil_image.verify()
        pil_image.transpose(Image.FLIP_LEFT_RIGHT)
        pil_image.close()
        img = cv2.imread(file_name)
    except Exception as e:
        print(e)
        img = None

    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def wrapper(storage_folder, images_folder):
    # get a list of the current stored images.
    # IGNORE files with the suffix .no as they are corrupted or reconstructed by the LASCO team, and the
    # interpolated data in inaccurate
    dirlisting = []
    path = os.path.join(storage_folder, "*.jpg")
    for name in glob.glob(path):
        name = os.path.normpath(name)
        seperator = os.path.sep
        n = name.split(seperator)
        nn = n[1]
        dirlisting.append(nn)

    # make sure they are in chronological order by name
    dirlisting.sort()
    t = dirlisting[0].split("_")
    hourcount = filehour_converter(t[0], t[1])
    hourimage = dirlisting[0]

    for i in range(0, len(dirlisting)):
        # split the name
        test = dirlisting[i].split("_")
        test_hourcount = filehour_converter(test[0], test[1])
        testimage = dirlisting[i]
        if test_hourcount - hourcount > (45 * 60):
            i1 = storage_folder + "/" + hourimage
            img_1 = image_load(i1)

            i2 = storage_folder + "/" + testimage
            img_2 = image_load(i2)

            # try:
            img_og = greyscale_img(img_1)
            img_ng = greyscale_img(img_2)

            # convert image to a single channel
            img_ng = cv2.split(img_ng)
            img_og = cv2.split(img_og)
            img_ng = img_ng[0]
            img_og = img_og[0]

            # improved histogram function
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
            img_og = clahe.apply(img_og)
            img_ng = clahe.apply(img_ng)

            # unary operator to invert the image
            img_ng = ~img_ng

            # combine the images to highlight differences
            alpha = 1
            gamma = 0
            new_image = img_ng.copy()
            cv2.addWeighted(img_ng, alpha, img_og, 1 - alpha, gamma, new_image)

            # Adjust contrast and brightness
            d = new_image.copy()
            alpha = 1.2
            beta = -50
            # alpha = 1.2
            # beta = -30
            new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)

            new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_BONE)

            # Save the difference image into the images folder
            add_stamp("Processed at Dunedin Aurora", new_image, hourimage)
            fname = images_folder + "/" + dirlisting[i]
            image_save(fname, new_image)
            # print("Display image created..." + fname)

            # LASTLY.....
            hourcount = test_hourcount
            hourimage = testimage
            # except:
            #     print("Unable to proces image")
    #
    # t = dirlisting[0].split("_")
    # hourcount = filehour_converter(t[0], t[1])
    # hourimage = dirlisting[0]
    #
    # for i in range(0, len(dirlisting)):
    #     # split the name
    #     test = dirlisting[i].split("_")
    #     test_hourcount = filehour_converter(test[0], test[1])
    #     testimage = dirlisting[i]
    #     if test_hourcount - hourcount > (45*60):
    #         i1 = storage_folder + "/" + hourimage
    #         img_1 = image_load(i1)
    #
    #         i2 = storage_folder + "/" + testimage
    #         img_2 = image_load(i2)
    #
    #         try:
    #             img_og = greyscale_img(img_1)
    #             img_ng = greyscale_img(img_2)
    #
    #             # convert image to a single channel
    #             img_ng = cv2.split(img_ng)
    #             img_og = cv2.split(img_og)
    #             img_ng = img_ng[0]
    #             img_og = img_og[0]
    #
    #             # img_og = erode_dilate_img(img_og)
    #             # img_ng = erode_dilate_img(img_ng)
    #
    #             # improved histogram function
    #             clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
    #             img_og = clahe.apply(img_og)
    #             img_ng = clahe.apply(img_ng)
    #
    #             # unary operator to invert the image
    #             img_ng = ~img_ng
    #
    #             # combine the images to highlight differences
    #             alpha = 1
    #             gamma = 0
    #             new_image = img_ng.copy()
    #             cv2.addWeighted(img_ng, alpha, img_og, 1 - alpha, gamma, new_image)
    #
    #             # Adjust contrast and brightness
    #             d = new_image.copy()
    #             alpha = 1.2
    #             beta = -50
    #             # alpha = 1.2
    #             # beta = -30
    #             new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)
    #
    #             new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_BONE)
    #
    #             # Save the difference image into the images folder
    #             add_stamp("Processed at Dunedin Aurora", new_image, hourimage)
    #             fname = images_folder + "/" + dirlisting[i]
    #             image_save(fname, new_image)
    #             # print("Display image created..." + fname)
    #
    #             # LASTLY.....
    #             hourcount = test_hourcount
    #             hourimage = testimage
    #         except:
    #             print("Unable to proces image")
