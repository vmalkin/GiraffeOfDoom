# -*- coding: utf-8 -*-
import cv2
import numpy as np

imgfolder = ''
# open an image
# https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg
#img = cv2.imread(imgfolder + 'test.jpg')
img = cv2.imread(imgfolder + 'latest_512_0193.jpg')
mask = cv2.imread(imgfolder + 'mask_black.bmp', 0)
#mask_red = cv2.imread(imgfolder + 'mask.bmp',0)

# converting an Image to grey scale...
greyimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Identify dark coronal hole areas from the solar surface...
# This is crude at the moment, but it basically works
ret, outputimg = cv2.threshold(greyimg, 25,255, cv2.THRESH_BINARY)

# Erode and Dilate the image to clear up noise
# Erosion will trim away pixels (noise)
# dilation puffs out edges
kernel = np.ones((5,5),np.uint8)
outputimg = cv2.erode(outputimg,kernel,iterations = 2)
outputimg = cv2.dilate(outputimg,kernel,iterations = 1)

# Mask off the blowout due to the corona
outputimg = cv2.bitwise_and(outputimg,outputimg,mask = mask)

# Save adjusted image
cv2.imwrite(imgfolder + 'saved.bmp', outputimg)
print("Done!")
