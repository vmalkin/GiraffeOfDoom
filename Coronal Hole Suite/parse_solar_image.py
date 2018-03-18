# -*- coding: utf-8 -*-
import cv2
import numpy as np
import urllib.request


def greyscale_img(image_to_process):
    # converting an Image to grey scale...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
    return greyimg

def threshold_img(image_to_process):
    # Identify dark coronal hole areas from the solar surface...
    # This is crude at the moment, but it basically works
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

if __name__ == '__main__':
    try:
        # open an image
        # https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg
        URL = 'https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg'
        
        with urllib.request.urlopen(URL) as url:
            with open('sun.jpg', 'wb') as f:
                f.write(url.read())
          
        img = cv2.imread('sun.jpg')
        
        # when saved in paint, a 16bit bmp seems ok
        mask1 = cv2.imread('mask_full.bmp', 0)
        mask2 = cv2.imread('mask1.bmp', 0)
    
        print(str(mask1.dtype) + " " + str(mask1.shape))
        print(str(mask2.dtype) + " " + str(mask2.shape))
    
            
        outputimg = greyscale_img(img)
        outputimg = threshold_img(outputimg)
        outputimg = erode_dilate_img(outputimg)
        
        try:
            outputimg1 = mask_img(outputimg, mask1)
            cv2.imwrite('disc_full.bmp', outputimg1)
        except:
            print("Unable to write image")
        
        try:
            outputimg2 = mask_img(outputimg, mask2)
            cv2.imwrite('disc_segment.bmp', outputimg2)
        except:
            print("Unable to write image")
        
        print("Done!")
    
    except:
        print("Unable to open URL")