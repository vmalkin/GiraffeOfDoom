import time
import cv2
import numpy as np
import datetime
from PIL import Image

averaging_iterations = 10
highpass_threshold = 3
current_camera = 2
blob_size = 4


def image_load(file_name):
    # Return a None if the image is currupt
    pil_image = Image.open(file_name)
    return pil_image


def test_blobs(image):
    # set up simple blob detector
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 2
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(image)
    print(keypoints)


def test_pixelcount(image):
    pixel_count = cv2.countNonZero(image)
    if pixel_count >= blob_size:
        print("Pixel count: ", pixel_count)


if __name__ == '__main__':
    testimage = image_load("test.jpg")
    testimage = np.array(testimage, np.uint8)

    # cv2.imshow('Input', test)
    # c = cv2.waitKey()
    # if c == 27:
    #     pass

    test_blobs(testimage)
    test_pixelcount(testimage)

