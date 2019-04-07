import cv2
import math
import numpy


cap = cv2.VideoCapture(0)


def setup_cam():
    # Change the camera setting using the set() function
    print(cv2.CAP_PROP_XI_DEVICE_SN)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    cap.set(cv2.CAP_PROP_GAIN, 255)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 188.0)
    cap.set(cv2.CAP_PROP_CONTRAST, 120)
    cap.set(cv2.CAP_PROP_HUE, 13)  # 13.0
    cap.set(cv2.CAP_PROP_SATURATION, 128)
    cap.set(cv2.CAP_PROP_EXPOSURE, -7)

if __name__ == ("__main__"):
    setup_cam()
    # # Read the current setting from the camera
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    contrast = cap.get(cv2.CAP_PROP_CONTRAST)
    saturation = cap.get(cv2.CAP_PROP_SATURATION)
    hue = cap.get(cv2.CAP_PROP_HUE)
    gain = cap.get(cv2.CAP_PROP_GAIN)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

    total_pixels = width * height

    # print("Test: ", test)
    # print("Ratio: ", ratio)
    # print("Frame Rate: ", frame_rate)
    print("Height: ", height)
    print("Width: ", width)
    print("Brightness: ", brightness)
    print("Contrast: ", contrast)
    print("Saturation: ", saturation)
    print("Hue: ", hue)
    print("Gain: ", gain)
    print("Exposure: ", exposure)


    # if cap.isOpened() == True:
    #     count_b_old = 0
    #     while True:
    #         ret, img = cap.read()
    #         if ret == True:
    #             greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #             count_b = cv2.countNonZero(greyimg)
    #
    #             k = 0.05
    #             count_b_old = (k * count_b) + ((1 - k) * count_b_old)
    #
    #             # if count_b > threshold:
    #             print((count_b_old / total_pixels))
    #                 # cv2.imwrite("image.png", img)

    if cap.isOpened() == True:
        ret, img = cap.read()
        if ret == True:
            greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            count_b = cv2.countNonZero(greyimg)
            cv2.imwrite("image.png", img)
        cap.release()
        cv2.destroyAllWindows()