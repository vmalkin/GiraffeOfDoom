# -*- coding: utf-8 -*-
# Solar Image Parser v0.1
# Designed to process an EUV image from a live URL 
# to display probably coronal hole locations. 
# uses the OpenCV library and based on the work of Rotter, Veronig, Temmer & Vrsnak
# http://oh.geof.unizg.hr/SOLSTEL/images/dissemination/papers/Rotter2015_SoPh290_arxiv.pdf

import cv2
import numpy as np
import urllib.request
import datetime
import time
from decimal import Decimal, getcontext
import logging
import common_data

# setup error logging
# logging levels in order of severity:
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

getcontext().prec = 6

class SolarImageProcessor:
    def __init__(self):
        self.coverage = 0


    # ##############
    # M E T H O D S
    # ##############
    def _image_read(self, file_name):
        img = cv2.imread(file_name)
        return img

    def _image_write(self, file_name, image_name):
        cv2.imwrite(file_name, image_name)

    def _get_utc_time(self):
        # returns a STRING of the current UTC time
        time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        return time_now

    def _calc_histo(self, image_to_process):
        hist = cv2.calcHist([image_to_process], [0], None, [256], [0, 256])
        print(hist)

    def _greyscale_img(self, image_to_process):
        # converting an Image to grey scale...
        greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
        return greyimg

    def _threshold_img(self, image_to_process):
        # Identify dark coronal hole areas from the solar surface...
        # This is crude at the moment, but it basically works
        # We will probably want to check the histogram for the image to define this
        # correctly. See original paper.
        ret, outputimg = cv2.threshold(image_to_process, 8, 255, cv2.THRESH_BINARY)
        return outputimg

    def _erode_dilate_img(self, image_to_process):
       # Erode and Dilate the image to clear up noise
        # Erosion will trim away pixels (noise)
        # dilation puffs out edges
        kernel = np.ones((5,5),np.uint8)
        outputimg = cv2.erode(image_to_process,kernel,iterations = 2)
        outputimg = cv2.dilate(outputimg,kernel,iterations = 1)
        return outputimg

    def _mask_img(self, image_to_process, maskname):
        # Mask off the blowout due to the corona
        outputimg = cv2.bitwise_and(image_to_process, image_to_process, mask = maskname)
        return outputimg

    def _count_pixels(self, part_img, whole_img):
        # compare the ratio of pixels between two images to derive
        # the area occupied by coronal holes
        total_pixels = cv2.countNonZero(whole_img)
        remainder_pixels = cv2.countNonZero(part_img)
        coverage = 1 - (Decimal(remainder_pixels) / Decimal(total_pixels))
        return coverage

    def _make_mask(self, mask_filepath):
        mask = cv2.imread(mask_filepath, 0)
        return mask

    def _add_img_logo(self, image_name):
        label = 'DunedinAurora.NZ Coronal Hole Map'
        label2 = self._get_utc_time()
        cv2.putText(image_name, label, (10,482), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(250,250,250), 1 );
        cv2.putText(image_name, label2, (10,498), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(250,250,250), 1 );
        # cv2.imwrite('disc_full.bmp', image_name)
        return image_name

    def _save_image_from_url(self, imageurl, filename):
        logging.debug("starting image from URL download: " + filename)
        try:
            request = urllib.request.Request(imageurl, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(request, timeout=10)
            with open(filename, 'wb') as f:
                f.write(response.read())
        except urllib.request.HTTPError:
            logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))


    # ################################
    # W R A P P E R   F U N C T I O N
    # ################################
    def get_meridian_coverage(self):
        try:
            self._save_image_from_url('https://services.swpc.noaa.gov/images/synoptic-map.jpg', 'syntopic.jpg')
        except:
            logging.debug("Unable to get syntopic map from NOAA")
            common_data.report_string = common_data.report_string + "Unable to get syntopic map from NOAA.\n"

        try:
            # self._save_image_from_url("https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg", "sun.jpg")
            self._save_image_from_url("https://services.swpc.noaa.gov/images/suvi-primary-195.png", "sun.jpg")

            img = self._image_read('sun.jpg')

            # current UTC time
            # nowtime_utc = get_utc_time()
            # nowtime_posix = get_posix_time()

            # when saved in paint, a 16bit bmp seems ok
            # # SDO masks
            # mask_full = self._make_mask('mask_full.bmp')
            # mask_segment = self._make_mask('mask_meridian.bmp')
            # GOES masks
            mask_full = self._make_mask('mask_full_goes.bmp')
            mask_segment = self._make_mask('mask_meridian_goes.bmp')

            # # print mask parameters for debugging purposes.
            # print(str(mask_full.dtype) + " " + str(mask_full.shape))
            # print(str(mask_segment.dtype) + " " + str(mask_segment.shape))

            # Process the image to get B+W coronal hole image
            outputimg = self._greyscale_img(img)
            outputimg = self._threshold_img(outputimg)
            outputimg = self._erode_dilate_img(outputimg)

            # save out the masked images

            # Full disk image
            outputimg1 = self._mask_img(outputimg, mask_full)

            # HERE we need to calculate the latitude of black pixels and account for dimishing effects cause by
            # increased latitude

            # Start grabbing all processed images and save as jpg
            try:
                time_now = str(datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M"))
                filename = "sun_jpegs/" + time_now + ".jpg"
                # filename = "sun_jpegs/" + str(int(time.time())) + ".jpg"
                self._image_write(filename, outputimg1)
            except:
                logging.error("Unable to process running solar image in JPG folder")
                print("Unable to process running solar image in JPG folder")


            self._add_img_logo(outputimg1)
            self._image_write('disc_full.bmp', outputimg1)

            # Meridian Segment
            outputimg2 = self._mask_img(outputimg, mask_segment)
            self._image_write('disc_segment.bmp', outputimg2)

            # Calculate the area occupied by coronal holes
            self.coverage = self._count_pixels(outputimg2, mask_segment)

            # It is extremely unlikely that we will ever get 100% coronal hole coverage on the meridian
            # Most ikely it is a glitched image from SDO - so we get less statistical grief if we reset the value
            # to a zero.
            if self.coverage == 1:
                self.coverage = 0

        except:
            logging.error("Unable to process SDO image")
            common_data.report_string = common_data.report_string + "Unable to calculate coronal hole coverage.\n"
            self.coverage = 0

