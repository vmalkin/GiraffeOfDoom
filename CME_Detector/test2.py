import cv2
import numpy as np

def image_load(file_name):
    img = cv2.imread(file_name)
    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


img = image_load("20210510_0954_c3_1024.jpg")

d = img.copy()
alpha = 2
beta = -180
new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)

cv2.imshow("test", new_image)
# Wait until user press some key
cv2.waitKey()