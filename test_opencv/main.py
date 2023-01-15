import cv2
import numpy as np
import math

# Automatically load images as greyscale with the zero flag!
img_1 = cv2.imread("20230115_1018_c3_1024.jpg", 0)
img_2 = cv2.imread("20230115_1030_c3_1024.jpg", 0)
img_3 = cv2.imread("20230115_1042_c3_1024.jpg", 0)
img_4 = cv2.imread("20230115_1054_c3_1024.jpg", 0)

cols = int(img_1.shape[0])
rows = int(img_1.shape[1])

threshold = 100

for i in range(0, cols):
    for j in range(0, rows):
        x = int(img_2[i][j]) - int(img_1[i][j])
        x = x * x
        x = int(math.sqrt(x))
        if x > threshold:
            print(x)


cv2.imshow('Grayscale Image', img_1)
cv2.waitKey(0)

cv2.imshow('Grayscale Image', img_2)
cv2.waitKey(0)

# cv2.imshow('Grayscale Image', img_3)
# cv2.waitKey(0)
#
# cv2.imshow('Grayscale Image', img_4)
# cv2.waitKey(0)
