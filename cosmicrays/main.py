import cv2
import numpy as np


averaging_iterations = 300


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
    camera = cv2.VideoCapture(0)
    camera_setup_c270(camera)
    print("Exposure: ", camera.get(cv2.CAP_PROP_EXPOSURE))


    averaging_array = []
    while True:
        ret, image = camera.read()
        img_g = greyscale_img(image)

        # Create an array of pictures with which to create an average
        pic = np.array(img_g, np.float64)
        averaging_array.append(pic)

        if len(averaging_array) >= averaging_iterations:
            # ALWAYS POP
            averaging_array.pop(0)
            avg_img = np.mean(averaging_array, axis=0)
            # print(avg_img)
            # detrended_img = cv2.subtract(pic, avg_img)
            detrended_img = pic - avg_img
            cv2.imshow('Input', detrended_img)

        c = cv2.waitKey(1)
        if c == 27:
            break

    camera.release()
    # cv2.destroyAllWindows()