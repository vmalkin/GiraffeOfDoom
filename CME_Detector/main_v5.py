import datetime
import time
import urllib.request
import pickle
import os
import cv2
import numpy as np


def get_resource_from_url(url_to_get):
    try:
        request = urllib.request.Request(url_to_get, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=10)

    except urllib.request.HTTPError:
        # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
        print("unable to load URL")
        print(url_to_get)
        response = ""
    return response


def load_values(pickle_file):
    returnvalue = variables
    if os.path.exists(pickle_file) is True:
        try:
            returnvalue = pickle.load(open(pickle_file, "rb"))
        except EOFError:
            print("Pickle file is empty")
    return returnvalue


def save_values(save_value, pickle_file):
    pickle.dump(save_value, open(pickle_file, "wb"), 0)


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def parse_image_fromURL(response, img_latest):
    with open(img_latest, 'wb') as f:
        f.write(response.read())


def parse_text_fromURL(response):
    # the response is a list of byte objects.
    returnlist = []
    for line in response:
        s = str(line)
        s = s.strip()
        s = s[2:27]
        returnlist.append(s)
    return returnlist


def image_load(file_name):
    img = cv2.imread(file_name)
    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def greyscale_img(image_to_process):
    # converting an Image to grey scale...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
    return greyimg


def erode_dilate_img(image_to_process):
    # Erode and Dilate the image to clear up noise
    # Erosion will trim away pixels (noise)
    # dilation puffs out edges
    kernel1 = np.ones((2, 2), np.uint8)
    outputimg = cv2.erode(image_to_process, kernel1, iterations=1)
    kernel2 = np.ones((1, 1), np.uint8)
    outputimg = cv2.dilate(outputimg, kernel2, iterations=1)
    return outputimg


def add_stamp(image_object):
    cv2. rectangle(image_object, (0, 900), (1024,1024), (255,255,255), -1 )
    colour = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1.0
    font_color = colour
    font_thickness = 2
    banner = 'DunedinAurora.NZ'
    x, y = 10, 925
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    font_size = 0.7
    font_color = colour
    font_thickness = 1
    banner = 'Courtesy of SOHO/LASCO consortium. SOHO is a project of'
    x, y = 10, 950
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'international cooperation between ESA and NASA'
    x, y = 10, 975
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


def filehour_converter(hhmm):
    hour = int(hhmm[:2])
    min = int(hhmm[2:])
    returnvalue = (hour * 60) + min
    return returnvalue


def processimages(listofimages):
    t = listofimages[0].split("_")
    hourcount = filehour_converter(t[1])
    hourimage = listofimages[0]

    for i in range(0, len(listofimages)):
        # split the name
        test = listofimages[i].split("_")
        test_hourcount = filehour_converter(test[1])
        testimage = listofimages[i]

        if test_hourcount - hourcount > 45:
            img1url = baseURL + hourimage
            img2url = baseURL + testimage

            response1 = get_resource_from_url(img1url)
            parse_image_fromURL(response1, "i1.bmp")
            img_1 = image_load("i1.bmp")

            response2 = get_resource_from_url(img2url)
            parse_image_fromURL(response2, "i2.bmp")
            img_2 = image_load("i2.bmp")

            img_og = greyscale_img(img_1)
            img_ng = greyscale_img(img_2)

            img_oe = erode_dilate_img(img_og)
            img_ne = erode_dilate_img(img_ng)

            # unary operator to invert the image
            img_ne = ~img_ne

            # combine the images to highlight differences
            alpha = 1.1
            gamma = 0
            new_image = img_ne.copy()
            cv2.addWeighted(img_ne, alpha, img_oe, 1 - alpha, gamma, new_image)

            # Adjust contrast and brightness
            d = new_image.copy()
            alpha = 1.2
            beta = -64
            new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)
            new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_TWILIGHT)

            # Save the difference image into the images folder
            add_stamp(new_image)
            fname = images_folder + "/" + listofimages[i]
            image_save(fname, new_image)
            print("Difference file created..." + fname)

            # LASTLY.....
            hourcount = test_hourcount
            hourimage = testimage



def parseimages(listofimages, variables):
    returnlist = []
    currenthour = variables["hour"]
    last =None
    for item in listofimages:
        i = item.split("_")
        t = i[1]
        if t > currenthour:
            returnlist.append(item)
            variables["hour"] = t
    return returnlist


if __name__ == "__main__":
    images_folder = "images"
    saved_variables = "variables.pkl"
    variables = None

    if os.path.exists(images_folder) is False:
        os.makedirs(images_folder)

    # if we dont have a pkl file, create one with default values.
    if os.path.exists(saved_variables) is False:
        variables = {
            "hour": "0000",
            "epoch": "20210517"
        }
        save_values(variables, saved_variables)
    else:
        variables = load_values(saved_variables)
    tm = int(time.time())

    # These need to be stored in program variables dictionary
    epoch = posix2utc(tm, "%Y%m%d")
    year = posix2utc(tm, "%Y")

    # if the current epoch is more recent that teh stored epoch
    # create online list for stored epoch
    # get the file list from online
    # parse for new images since the last parse
    # process and store new images
    # Update the variables file with the current epoch and file number
    #
    # If the current epoch equals the stored epoch
    # get the file list from online
    # parse for new images since the last parse
    # process and store new images
    # Update the variables file with the file number

    if epoch > variables["epoch"]:
        print("old epoch, update variables")
        ymd = variables["epoch"]
        baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd + "/"
        onlinelist = baseURL + ".full_1024.lst"
        print(onlinelist)
        listofimages = get_resource_from_url(onlinelist)
        listofimages = parse_text_fromURL(listofimages)
        newimages = parseimages(listofimages, variables)

        if len(newimages) > 0:
            processimages(newimages)

        print(newimages)
        print(variables)

        variables["epoch"] = epoch
        variables["hour"] = "0000"

        save_values(variables, saved_variables)

    if epoch == variables["epoch"]:
        ymd = variables["epoch"]
        baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd + "/"
        onlinelist = baseURL + ".full_1024.lst"
        print(onlinelist)
        listofimages = get_resource_from_url(onlinelist)
        listofimages = parse_text_fromURL(listofimages)
        newimages = parseimages(listofimages, variables)

        if len(newimages) > 0:
            processimages(newimages)

        print(newimages)
        print(variables)

        # we save here as there could be updates to the hour variable
        save_values(variables, saved_variables)
