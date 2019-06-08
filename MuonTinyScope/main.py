import cv2
import math
import numpy
import time
import datetime

cap = cv2.VideoCapture(0)
logfile = "strikes.csv"

def setup_cam():
    # Change the camera setting using the set() function
    print(cv2.CAP_PROP_XI_DEVICE_SN)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_GAIN, 255)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 240)
    cap.set(cv2.CAP_PROP_CONTRAST, 255)
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


    if cap.isOpened() == True:
        count_b_old = 0
        counter = 0
        max_value = 0
        while True:
            ret, img = cap.read()
            if ret == True:
                counter  = counter + 1
                greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                count_b = cv2.countNonZero(greyimg)
                
                k = 0.1
                count_b_old = (k * count_b) + ((1 - k) * count_b_old)
                
                if count_b_old > max_value:
                    max_value = count_b_old

                if counter >= 100:
                    posix_time = time.time()
                    utc_time = datetime.datetime.utcfromtimestamp(int(posix_time)).strftime('%Y-%m-%d %H:%M:%S')
                    dp = str(int(posix_time)) + "," + str(utc_time) + "," + str(int(max_value))
                    print(dp)
                    with open(logfile, "a") as l:
                        l.write(dp + "\n")
                        l.close()

                    counter = 0
                    max_value = 0
                    
        cap.release()
        cv2.destroyAllWindows()
