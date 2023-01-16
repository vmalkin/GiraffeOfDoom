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

threshold = 20
# picture = np.zeros([cols, rows], np.uint8)
denoised = np.full([cols, rows], 50, np.uint8)
for i in range(0, rows):
    for j in range(0, cols):
        x = int(img_2[i][j]) - int(img_1[i][j])
        x = x * x
        x = int(math.sqrt(x))
        if x < threshold:
            denoised[i][j] = img_2[i][j]

picture = cv2.GaussianBlur(denoised, (3,3), 0)
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(10,10))
final1 = clahe.apply(picture)
final1 = cv2.bitwise_not(final1)

img_2 = cv2.bitwise_not(img_2)
cv2.imshow('img_2', img_2)

denoised = cv2.bitwise_not(denoised)
cv2.imshow('denoised', denoised)

cv2.imshow('final1', final1)
cv2.waitKey(0)



# cv2.imshow('Grayscale Image', img_3)
# cv2.waitKey(0)
#
# cv2.imshow('Grayscale Image', img_4)
# cv2.waitKey(0)
