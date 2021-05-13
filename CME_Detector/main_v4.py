import datetime
import time
import urllib.request
import pickle
import os
import cv2
import numpy as np

variables = {
    "img_stored": "20100101_0000_c3_1024.jpg"
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


# def parse_filename_fromURL(response):
#     # the response is a list of byte objects.
#     for line in response:
#         s = str(line)
#         s = s.strip()
#         # Parse out the file names from the HTML
#         try:
#             s = s.split('<a href="')
#             t = s[1]
#             t = t.split('">')
#             if t[0].find("1024") > 0:  # find 1024 scale images from list
#                 filename = t[0]
#         except:
#             pass
#     return filename


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
    cv2. rectangle(image_object, (0, 900), (1024,1024), (255,0,0), -1 )
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
    banner = 'Acknowledgement for Lasco/SOHO usage here'
    x, y = 10, 950
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


if __name__ == "__main__":
    images_folder = "images"
    if os.path.exists(images_folder) is False:
        os.makedirs(images_folder)

    # https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/2021/c3/20210509/.full_1024.lst
    tm = int(time.time())

    # These need to be stored in program variables dictionary
    yearmonthday = posix2utc(tm, "%Y%m%d")
    year = posix2utc(tm, "%Y")
    # baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + "20210512" + "/"
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + yearmonthday + "/"
    onlinelist = baseURL + ".full_1024.lst"
    print(onlinelist)
    saved_variables = "variables.pkl"

    # if we dont have a pkl file, create one with default values.
    if os.path.exists(saved_variables) is False:
        variables = {
            "img_stored": "20100101_0000_c3_1024.jpg"
        }
        save_values(variables, saved_variables)
    else:
        variables = load_values(saved_variables)

    # Get the catalogue of latest images from the website
    print(onlinelist)
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_fromURL(listofimages)

    # We want to grab the latest images that have been appended to the file list since the last time we looked at it
    # we will use the name of the last file we processed stored in variables[] help us.
    new_images_list = []
    v = variables["img_stored"].split("_")
    vv = int(v[0] + v[1])
    last = ""
    for item in listofimages:
        u = item.split("_")
        uu = int(u[0] + u[1])
        if uu > vv:
            new_images_list.append(item)

    # We can now process these new images stored in the temp array.
    if len(new_images_list) > 0:
        t =  new_images_list[0].split("_")
        hourcount = int(t[1])
        hourimage = new_images_list[0]

        for i in range(0, len(new_images_list)):
            # split the name
            test = new_images_list[i].split("_")
            test_hourcount = int(test[1])
            testimage = new_images_list[i]

            if test_hourcount - hourcount > 100:
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
                alpha = 0.8
                gamma = 0
                new_image = img_ne.copy()
                cv2.addWeighted(img_ne, alpha, img_oe, 1 - alpha, gamma, new_image)

                # Adjust contrast and brightness
                d = new_image.copy()
                alpha = 2
                beta = -180
                new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)

                # Save the difference image into the images folder
                add_stamp(new_image)
                fname = images_folder + "/" + listofimages[i]
                image_save(fname, new_image)
                print("Difference file created...")

                # LASTLY.....
                hourcount = test_hourcount
                hourimage = testimage

            last = listofimages[i]
        variables["img_stored"] = last
        print(variables)
        save_values(variables, saved_variables)
    else:
        print(variables)
        print("No new images to download.")

