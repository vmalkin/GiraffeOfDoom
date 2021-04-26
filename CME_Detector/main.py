import cv2
import numpy as np
import urllib.request
import time
import os

url_lasco_c3 = "https://soho.nascom.nasa.gov/data/realtime/c3/1024/latest.jpg"
t = int(time.time())
img_stored = "lasco.bmp"
img_latest = "latest.bmp"
# img_latest = "lasco.jpg"


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
    kernel = np.ones((5,5),np.uint8)
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

# img1 = image_load(img_test)
# img2 = image_load(img_latest)
#
# img1 = greyscale_img(img1)
# img2 = greyscale_img(img2)
#
# img1 = erode_dilate_img(img1)
# img2 = erode_dilate_img(img2)
#
# diff = img1.copy()
# cv2.absdiff(img1, img2, diff)
#
# alpha = 15
# beta = 20
# new_image = cv2.convertScaleAbs(diff, alpha=alpha, beta=beta)
#
#
# image_save("diff.jpg", new_image)

# cv2.imshow("Diffs", new_image)
# cv2.waitKey(0)  # waits until a key is pressed
# cv2.destroyAllWindows()  # destroys the window showing image

if __name__ == "__main__":
    result = get_image_from_url()

    if result == "success":
        # if there is no storted image ie: the first time the program has run, save the latest image as
        # the new stored image and stop.
        print("SUCCESS - Data downloaded from URL")
        if os.path.isfile(img_stored) == False:
            i = image_load(img_latest)
            image_save(img_stored, i)
            print("No stored file. Created new stored image.")

        img_s = image_load(img_stored)
        img_l = image_load(img_latest)

        img_sg = greyscale_img(img_s)
        img_lg = greyscale_img(img_l)

        img_se = erode_dilate_img(img_sg)
        img_le = erode_dilate_img(img_lg)

        diff = img_s.copy()
        cv2.absdiff(img_s, img_l, diff)

        # test to see if there is a difference between the two images if so, the latest
        # image is the new current image to save for the next comparison
        image_difference = np.sum(diff)
        print(image_difference)
        if image_difference > 0:
            alpha = 15
            beta = 20
            new_image = cv2.convertScaleAbs(diff, alpha=alpha, beta=beta)

            # Save the difference image
            image_save("diff.jpg", new_image)

            # Parse for edges - identify CME?

            # save the latest image as the new current image
            image_save(img_latest, img_s)
            print("Difference in images detected. Difference file created.")
        else:
            print("New image from internet is the same as stored image. No difference calculated")
    else:
        print("FAIL - Unable to load new image from URL")
