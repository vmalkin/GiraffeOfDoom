import cv2

img_1 = cv2.imread("20230115_1018_c3_1024.jpg", 0)
img_2 = cv2.imread("20230115_1030_c3_1024.jpg", 0)
img_3 = cv2.imread("20230115_1042_c3_1024.jpg", 0)
img_4 = cv2.imread("20230115_1054_c3_1024.jpg", 0)

cv2.imshow('Grayscale Image', img_1)
cv2.waitKey(0)

cv2.imshow('Grayscale Image', img_2)
cv2.waitKey(0)

cv2.imshow('Grayscale Image', img_3)
cv2.waitKey(0)

cv2.imshow('Grayscale Image', img_4)
cv2.waitKey(0)