#  fix opencv error in windows with:
#  https://stackoverflow.com/questions/63869389/error-could-not-build-wheels-for-opencv-python-which-use-pep-517-and-cannot-b

import cv2 as cv
import numpy as np

if __name__ == '__main__':
    img1 = cv.imread("or_suvi-l2-ci171_g18_s20230525T224000Z_e20230525T224400Z_v1-0-1.png", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("or_suvi-l2-ci171_g18_s20230525T224400Z_e20230525T224800Z_v1-0-1.png", cv.IMREAD_GRAYSCALE)

    imgd = img2 - img1
    cv.imwrite("diff.jpg", imgd)
    # cv.imshow('unchanged image', imgd)
    # cv.waitKey(0)
    # cv.destroyAllwindows()


