import datetime
import time
import urllib.request
import pickle
import os
import cv2
import numpy as np


baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/2021/c3/"
variables = {
    "img_stored" : ""
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


if __name__ == "__main__":
    t = int(time.time())
    yearmonthday = posix2utc(t, "%Y%m%d")
    # hourmin = posix2utc(t, "%H%M")
    program_variables = "variables.pkl"
    image_current = "current.bmp"
    variables = load_values(program_variables)
    toget = baseURL + yearmonthday

    # get list of files from Lasco website. get the most recent filename from said list...
    response = get_resource_from_url(toget)
    img_latest = parse_filename_fromURL(response)

    # if the latest filename is different to the latest stored value, this is a new image
    if variables["img_stored"] != img_latest:
        variables["img_stored"] = img_latest  # Update the stored value with the new filename

        imageURL = baseURL + yearmonthday + "/" + img_latest
        print(imageURL)
        response = get_resource_from_url(imageURL)
        parse_image_fromURL(response, "temp.bmp")

        if os.path.exists(image_current) is False:
            print("No current image, saving one...")
            i = image_load("temp.bmp")
            image_save(image_current, i)

        img_old = image_load(image_current)
        img_new = image_load("temp.bmp")

        img_og = greyscale_img(img_old)
        img_ng = greyscale_img(img_new)

        img_oe = erode_dilate_img(img_og)
        img_ne = erode_dilate_img(img_ng)

        diff = img_oe.copy()
        cv2.absdiff(img_oe, img_ne, diff)

        # test to see if there is a difference between the two BASE images if so, the latest
        # image is the new current image to save for the next comparison
        image_difference = np.sum(diff)

        if image_difference > 0:
            print("Difference detected: ")
            print(image_difference)
            alpha = 10
            beta = 10
            new_image = cv2.convertScaleAbs(diff, alpha=alpha, beta=beta)

            # Save the difference image
            add_stamp(new_image)
            timelapse = posix2utc(time.time(), '%Y_%m_%d_%H_%M')
            fname = timelapse + ".jpg"
            image_save(fname, new_image)
            print("Difference in images detected. Difference file created.")

        # Update the program variables file
        save_values(variables, program_variables)

    else:
        print("No new update to online images")



