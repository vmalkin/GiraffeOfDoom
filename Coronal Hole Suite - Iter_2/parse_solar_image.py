# -*- coding: utf-8 -*-
# Solar Image Parser v0.1
# Designed to process an EUV image from a live URL 
# to display probably coronal hole locations. 
# uses the OpenCV library and based on the work of Rotter, Veronig, Temmer & Vrsnak
# http://oh.geof.unizg.hr/SOLSTEL/images/dissemination/papers/Rotter2015_SoPh290_arxiv.pdf

import cv2
import numpy as np
#import urllib.request
import datetime
from decimal import Decimal, getcontext
import logging

# setup error logging
# logging levels in order of severity:
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

getcontext().prec = 6

def image_read(file_name):
    img = cv2.imread(file_name)
    return img

def image_write(file_name, image_name):
    cv2.imwrite(file_name, image_name)

def get_utc_time():
    # returns a STRING of the current UTC time
    time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    return time_now

def calc_histo(image_to_process):
    hist = cv2.calcHist([image_to_process], [0], None, [256], [0, 256])
    print(hist)

def greyscale_img(image_to_process):
    # converting an Image to grey scale...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
    return greyimg

def threshold_img(image_to_process):
    # Identify dark coronal hole areas from the solar surface...
    # This is crude at the moment, but it basically works
    # We will probabbly want to check the histogram for the image to define this
    # correctly. See original paper.
    ret, outputimg = cv2.threshold(image_to_process, 15,255, cv2.THRESH_BINARY)
    return outputimg

def erode_dilate_img(image_to_process):
   # Erode and Dilate the image to clear up noise
    # Erosion will trim away pixels (noise)
    # dilation puffs out edges
    kernel = np.ones((5,5),np.uint8)
    outputimg = cv2.erode(image_to_process,kernel,iterations = 2)
    outputimg = cv2.dilate(outputimg,kernel,iterations = 1) 
    return outputimg

def mask_img(image_to_process, maskname):
    # Mask off the blowout due to the corona
    outputimg = cv2.bitwise_and(image_to_process, image_to_process, mask = maskname)
    return outputimg

def count_pixels(part_img, whole_img):
    # compare the ratio of pixels between two images to derive
    # the area occupied by coronal holes
    total_pixels = cv2.countNonZero(whole_img)
    remainder_pixels = cv2.countNonZero(part_img)
    coverage = 1 - (Decimal(remainder_pixels) / Decimal(total_pixels))
    return coverage
      
def make_mask(mask_filepath):
    mask = cv2.imread(mask_filepath, 0)
    return mask
     
def add_img_logo(image_name):
    label = 'DunedinAurora.NZ Coronal Hole Map'
    label2 = get_utc_time()
    cv2.putText(image_name, label, (10,482), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(250,250,250), 1 );
    cv2.putText(image_name, label2, (10,498), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(250,250,250), 1 );
#    cv2.imwrite('disc_full.bmp', image_name)
    return image_name
