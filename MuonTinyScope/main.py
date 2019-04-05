import cv2
import numpy


cap = cv2.VideoCapture(0)

def setup_cam():
    # Change the camera setting using the set() function
    cap.set(cv2.CAP_PROP_GAIN, 4.0)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 140.0)
    cap.set(cv2.CAP_PROP_CONTRAST, 27.0)
    cap.set(cv2.CAP_PROP_HUE, 13)  # 13.0
    cap.set(cv2.CAP_PROP_SATURATION, 28.0)
    cap.set(cv2.CAP_PROP_EXPOSURE, 1)

if __name__ == ("__main__"):
    setup_cam()

    # Read the current setting from the camera
    test = cap.get(cv2.CAP_PROP_POS_MSEC)
    ratio = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    contrast = cap.get(cv2.CAP_PROP_CONTRAST)
    saturation = cap.get(cv2.CAP_PROP_SATURATION)
    hue = cap.get(cv2.CAP_PROP_HUE)
    gain = cap.get(cv2.CAP_PROP_GAIN)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

    print("Test: ", test)
    print("Ratio: ", ratio)
    print("Frame Rate: ", frame_rate)
    print("Height: ", height)
    print("Width: ", width)
    print("Brightness: ", brightness)
    print("Contrast: ", contrast)
    print("Saturation: ", saturation)
    print("Hue: ", hue)
    print("Gain: ", gain)
    print("Exposure: ", exposure)

    while True:
        ret, img = cap.read()
        greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        count_b = cv2.countNonZero(greyimg)
        print("Non black pixels: " + str(count_b))
        # cv2.imwrite("image.png", greyimg)

    cap.release()