import cv2
import main_v6

img = main_v6.countpixels()


cv2.imshow("test", img)
# Wait until user press some key
cv2.waitKey()