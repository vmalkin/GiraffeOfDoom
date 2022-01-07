import cv2
import numpy as np

def camera_setup_c270(cam):
    """
    https://physicsopenlab.org/2016/05/18/diy-webcam-particle-detector/
    Resolution = 640 x 480
    Exposure = -7 (corresponding to 1/10 s)
    Gain = 255
    Sharp = 255
    """
    cam.set(cv2.CAP_PROP_GAIN, 255)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
    # # No
    # camera.set(cv2.CAP_PROP_GAMMA, 128)
    # Can set. 255 max value
    cam.set(cv2.CAP_PROP_SATURATION, 32)
    # camera.set(cv2.CAP_PROP_HUE, -1)
    cam.set(cv2.CAP_PROP_CONTRAST, 32)
    cam.set(cv2.CAP_PROP_SHARPNESS, 255)
    # Set to zero for auto exposure. Set to 1 for manual exposure
    # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, -12)
    # max of 10000 manually
    camera.set(cv2.CAP_PROP_EXPOSURE, 120)



if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    camera_setup_c270(camera)
    print("Exposure: ", camera.get(cv2.CAP_PROP_EXPOSURE))


    averaging_array = []
    while True:
        ret, image = camera.read()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', image)

        c = cv2.waitKey(1)
        if c == 27:
            break

    camera.release()
    # cv2.destroyAllWindows()