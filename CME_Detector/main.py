import cv2
import numpy as np
import urllib.request
import time
import datetime
import os
import json

url_lasco_c3 = "https://soho.nascom.nasa.gov/data/realtime/c3/1024/latest.jpg"
t = int(time.time())
img_stored = "lasco.bmp"
img_latest = "latest.bmp"


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


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
    kernel = np.ones((3,3),np.uint8)
    outputimg = cv2.erode(image_to_process,kernel,iterations = 1)
    outputimg = cv2.dilate(outputimg,kernel,iterations = 1)
    return outputimg


def get_image_from_url():
    result = "fail"
    try:
        request = urllib.request.Request(url_lasco_c3, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=10)

        with open(img_latest, 'wb') as f:
            f.write(response.read())
        result = "success"
    except urllib.request.HTTPError:
        # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
        print("unable to load image")
    return result

# cv2.imshow("Diffs", new_image)
# cv2.waitKey(0)  # waits until a key is pressed
# cv2.destroyAllWindows()  # destroys the window showing image
def add_stamp(image_object):
    colour = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 2.0
    font_color = colour
    font_thickness = 2
    banner = 'DunedinAurora.NZ'
    x, y = 10, 1000
    img_text = cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


def json_timestamper():
    # half an hour between attempts
    interval = 60 * 15
    intervaltimer = False
    nowtime = int(time.time())
    timejsonfile = "time.json"
    timejson = {"prev": nowtime,
                "now": nowtime}

    # create json file if it does not exist, else load json data
    if os.path.isfile(timejsonfile) is False:
        with open(timejsonfile, "w") as j:
            json.dump(timejson, j)
            intervaltimer = True
    else:
        with open(timejsonfile, "r") as j:
            timejson = json.load(j)


    # check to see if the interval has passed
    if nowtime - timejson["prev"] > interval:
        timejson["prev"] = nowtime
        timejson["now"] = nowtime
        intervaltimer = True
    else:
        timejson["now"] = nowtime

    # write updated nowtime to json file
    with open(timejsonfile, "w") as j:
        json.dump(timejson, j)
    print(timejson)
    return intervaltimer


if __name__ == "__main__":
    runnow = json_timestamper()
    print("Run-now is: " + str(runnow))

    if runnow is True:
        result = get_image_from_url()

        if result == "success":
            # if there is no storted image ie: the first time the program has run, save the latest image as
            # the new stored image and stop.
            print("SUCCESS - Data downloaded from URL")
            if os.path.isfile(img_stored) is False:
                i = image_load(img_latest)
                image_save(img_stored, i)
                print("No stored file. Created new stored image.")

            img_s = image_load(img_stored)
            img_l = image_load(img_latest)

            img_sg = greyscale_img(img_s)
            img_lg = greyscale_img(img_l)

            img_se = erode_dilate_img(img_sg)
            img_le = erode_dilate_img(img_lg)

            image_save("se.jpg", img_se)
            image_save("le.jpg", img_le)

            diff = img_s.copy()
            cv2.absdiff(img_s, img_l, diff)

            # test to see if there is a difference between the two BASE images if so, the latest
            # image is the new current image to save for the next comparison
            image_difference = np.sum(diff)

            print(image_difference)
            if image_difference > 0:
                diff = img_se.copy()
                cv2.absdiff(img_le, img_se, diff)

                alpha = 15
                beta = 20
                new_image = cv2.convertScaleAbs(diff, alpha=alpha, beta=beta)

                # Save the difference image
                add_stamp(new_image)
                timelapse = posix2utc(time.time(), '%Y_%m_%d_%H_%M')
                fname = timelapse + ".jpg"
                image_save(fname, new_image)
                print("Difference in images detected. Difference file created.")
                # Parse for edges - identify CME?

                # # save the latest image as the new current image
                # image_save(img_stored, img_l)
                # print("Latest image copied as LASCO current image")
            else:
                print("New image from internet is the same as stored image. No difference calculated")
        else:
            print("FAIL - Unable to load new image from URL")
