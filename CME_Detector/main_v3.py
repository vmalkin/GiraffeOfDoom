import datetime
import time
import urllib.request
import pickle
import os
import cv2
import numpy as np

# https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/2021/c3/20210509/.full_1024.lst


# baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/2021/c3/"
variables = {
    "img_stored" : "",
    "yearmonthday" : "",
    "year" : "",
    "onlinelist" : ""
}


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


def parse_filename_fromURL(response):
    # the response is a list of byte objects.
    for line in response:
        s = str(line)
        s = s.strip()
        # Parse out the file names from the HTML
        try:
            s = s.split('<a href="')
            t = s[1]
            t = t.split('">')
            if t[0].find("1024") > 0:  # find 1024 scale images from list
                filename = t[0]
        except:
            pass
    return filename


def parse_image_fromURL(response, img_latest):
    with open(img_latest, 'wb') as f:
        f.write(response.read())


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
    kernel1 = np.ones((1, 1), np.uint8)
    outputimg = cv2.erode(image_to_process, kernel1, iterations=1)
    kernel2 = np.ones((1, 1), np.uint8)
    outputimg = cv2.dilate(outputimg, kernel2, iterations=1)
    return outputimg


def add_stamp(image_object):
    colour = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 2.0
    font_color = colour
    font_thickness = 2
    banner = 'DunedinAurora.NZ'
    x, y = 10, 1000
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


def generalprocess():
    """This is a wrapper function for the general process of getting new data and processing it"""

    # get online list
    # check list names against recent stored name
    # if new names, reset resent stored name in program variables.
    # download images in pairs
    # process differences and save

    pass


if __name__ == "__main__":
    # https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/2021/c3/20210509/.full_1024.lst
    t = int(time.time())

    # These need to be stored in program variables dictionary
    yearmonthday = posix2utc(t, "%Y%m%d")
    year = posix2utc(t, "%Y")
    onlinelist = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + yearmonthday + "/.full_1024.lst"

    saved_variables = "variables.pkl"
    variables = load_values(saved_variables)

    # check UTC date agaainst stored date
    # if a new date, run check one last time against the old date just in case there was an update. Otherwise
    # update program variables to NEW values then proceed
    if variables["yearmonthday"] != yearmonthday:
        generalprocess(variables)

        variables["yearmonthday"] = yearmonthday
        variables["year"] = year
        variables["onlinelist"] = onlinelist
        save_values(variables, saved_variables)
    else:
        generalprocess(variables)










