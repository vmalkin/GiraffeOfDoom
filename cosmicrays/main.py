import time

import cv2
import numpy as np
import datetime

averaging_iterations = 5
highpass_threshold = 4
current_camera = 2


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def camera_setup_c270(cam):
    """
    https://physicsopenlab.org/2016/05/18/diy-webcam-particle-detector/
    Resolution = 640 x 480
    Exposure = -7 (corresponding to 1/10 s)
    Gain = 255
    Sharp = 255
    """
    cam.set(cv2.CAP_PROP_GAIN, 255)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 120)
    # # No
    # camera.set(cv2.CAP_PROP_GAMMA, 128)
    # Can set. 255 max value
    cam.set(cv2.CAP_PROP_SATURATION, 100)
    # camera.set(cv2.CAP_PROP_HUE, -1)
    cam.set(cv2.CAP_PROP_CONTRAST, 32)
    cam.set(cv2.CAP_PROP_SHARPNESS, 255)
    # Set to zero for auto exposure. Set to 1 for manual exposure
    # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, -12)
    # max of 10000 manually
    camera.set(cv2.CAP_PROP_EXPOSURE, 120)



def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    return greyimg


if __name__ == '__main__':
    averaging_array = []
    display_flag = True
    camera = cv2.VideoCapture(current_camera)
    camera_setup_c270(camera)

    print("Exposure: ", camera.get(cv2.CAP_PROP_EXPOSURE))
    sh_x = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    sh_y = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Frame size: ", sh_x, sh_y)

    # Create a highpass filter
    highpass = np.full((sh_y, sh_x), highpass_threshold)

    # Image to show accumulating stikes
    show_img = np.full((sh_y, sh_x), 0)

    # set up simple blob detector
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 4
    detector = cv2.SimpleBlobDetector_create(params)

    while True:
        ret, image = camera.read()
        # img_g = image
        img_g = greyscale_img(image)

        # Create an array of pictures with which to create an average
        # pic = np.array(img_g, np.float64)
        averaging_array.append(img_g)

        if len(averaging_array) >= averaging_iterations:
            # ALWAYS POP
            averaging_array.pop(0)
            avg_img = np.mean(averaging_array, axis=0)

            if display_flag == True:
                print("Max avg pixel value. Make threshold above this: ", np.median(avg_img))
                display_flag = False

            detrended_img = img_g - avg_img - highpass
            # Clip any value less than zero, to zero.
            # convert anything equal of over to 255
            detrended_img = np.where(detrended_img <= 0, 0,detrended_img)
            detrended_img = np.where(detrended_img > 0, 255, detrended_img)

            pixel_count = cv2.countNonZero(detrended_img)
            if pixel_count >= 3:
                print(t + " Pixelcount Fired! " + str(pixel_count) + " pixels")

            test = np.array(detrended_img, np.uint8)
            keypoints = detector.detect(test)
            if len(keypoints) > 0:
                n = t = posix2utc(time.time(), '%Y-%m-%d')
                filename = "CRays_" + n + ".jpg"
                show_img = show_img + detrended_img - highpass
                image_save(filename, show_img)
                t = posix2utc(time.time(), '%Y-%m-%d %H:%M')
                print(t + " Blob detected! " + str(pixel_count) + " pixels")
                cv2.imshow('Input', show_img)

        # c = cv2.waitKey(1)
        # if c == 27:
        #     break

    camera.release()
    cv2.destroyAllWindows()