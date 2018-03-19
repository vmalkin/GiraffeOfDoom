# -*- coding: utf-8 -*-
# Solar Image Parser v0.1
# Designed to process an EUV image from a live URL
# to display probably coronal hole locations. 
# uses the OpenCV library
# http://oh.geof.unizg.hr/SOLSTEL/images/dissemination/papers/Rotter2015_SoPh290_arxiv.pdf

import cv2
import numpy as np
import urllib.request
import datetime
from decimal import Decimal, getcontext
import time

getcontext().prec = 4

def get_utc():
    # returns a STRING of the current UTC time
    time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    return time_now

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
    
def record_coverage(value_string):
    pass

if __name__ == '__main__':
    while True:
        try:
            # open an image
            # https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg
            URL = 'https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg'
            
            with urllib.request.urlopen(URL) as url:
                with open('sun.jpg', 'wb') as f:
                    f.write(url.read())
              
            img = cv2.imread('sun.jpg')
            
            #current UTC time
            nowtime = get_utc()
            
            # when saved in paint, a 16bit bmp seems ok
            mask1 = cv2.imread('mask_full.bmp', 0)
            mask2 = cv2.imread('mask1.bmp', 0)
            
    #        # print mask parameters for debugging purposes.
    #        print(str(mask1.dtype) + " " + str(mask1.shape))
    #        print(str(mask2.dtype) + " " + str(mask2.shape))
        
            # Process the image to get B+W coronal hole image    
            outputimg = greyscale_img(img)
            outputimg = threshold_img(outputimg)
            outputimg = erode_dilate_img(outputimg)
            
            # save out the masked images
            try:
                # Full disk image
                outputimg1 = mask_img(outputimg, mask1)
                label = 'DunedinAurora.NZ Coronal Hole Map'
                label2 = nowtime
                cv2.putText(outputimg1, label, (10,482), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(250,250,250), 1 );
                cv2.putText(outputimg1, label2, (10,498), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(250,250,250), 1 );
                cv2.imwrite('disc_full.bmp', outputimg1)
            except:
                print("Unable to write image")
            
            try:
                # Meridian Segment
                outputimg2 = mask_img(outputimg, mask2)
                cv2.imwrite('disc_segment.bmp', outputimg2)
            except:
                print("Unable to write image")
               
        except:
            # URL access has malfunctioned??
            print("Unable to open URL")
        
        # Calculate the area occupied by coronal holes
        coverage = count_pixels(outputimg2, mask2)
        print(str(nowtime) + "," + str(coverage))
        # tie this in with solar sind speed and density data
        # create the incremental indice of CH activity.
    
        time.sleep(3600)