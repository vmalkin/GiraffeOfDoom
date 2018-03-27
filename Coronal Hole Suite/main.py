import datetime
import parse_discovr_data as discovr
import parse_solar_image as solar
import urllib.request
import os
import time

LOGFILE = 'log.csv'

def prune_logfile(filename):
    pass

def log_data(value_string):
    # If the logfile exists append the datapoint
    try:
        with open (LOGFILE,'a') as f:
            f.write(value_string + '\n')
            # print("Data logged ok. Array Size: " + str(len(readings)))
    except IOError:
        print("WARNING: There was a problem accessing the current logfile: " + LOGFILE)
    
def get_utc_time():
    # returns a STRING of the current UTC time
    time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    return time_now


 # #################################################################################
 # B E G I N   M A I N   H E R E 
 # #################################################################################   
if __name__ == '__main__':
    while True:
        # set up the logfile if it does not exist
        try:
            if not os.path.isfile(LOGFILE):
                log_data("UTC time, percent CH on Meridian, Wind speed, Particle density")
        except:
            print("Unable to create new log file")
            
        # prune the logfile if it too long.
        
        try:
            # open an image
            # https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg
            URL = 'https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg'
            
            with urllib.request.urlopen(URL) as url:
                with open('sun.jpg', 'wb') as f:
                    f.write(url.read())
              
            img = solar.image_read('sun.jpg')
            
            
            
            #current UTC time
            nowtime = get_utc_time()
            
            # when saved in paint, a 16bit bmp seems ok
            mask1 = solar.make_mask('mask_full.bmp')
            mask2 = solar.make_mask('mask1.bmp')
            
        #        # print mask parameters for debugging purposes.
        #        print(str(mask1.dtype) + " " + str(mask1.shape))
        #        print(str(mask2.dtype) + " " + str(mask2.shape))
            
            # Process the image to get B+W coronal hole image    
            outputimg = solar.greyscale_img(img)
            outputimg = solar.threshold_img(outputimg)
            outputimg = solar.erode_dilate_img(outputimg)
            
            # save out the masked images
            try:
                # Full disk image
                outputimg1 = solar.mask_img(outputimg, mask1)
                solar.add_img_logo(outputimg1)
                solar.image_write('disc_full.bmp', outputimg1)
            except:
                print("Unable to write image")
            
            try:
                # Meridian Segment
                outputimg2 = solar.mask_img(outputimg, mask2)
                solar.image_write('disc_segment.bmp', outputimg2)
            except:
                print("Unable to write image")
               
        except:
            # URL access has malfunctioned??
            print("Unable to open URL")
        
        # Calculate the area occupied by coronal holes
        coverage = solar.count_pixels(outputimg2, mask2)
        
        # #################################################################################
        # Get the DISCOVR solar wind data (speed and density)
        # We do need to check that data is timely!! Naive implementation at the moment
        # #################################################################################
        
        try:
            # get the data
            dscvr_data = discovr.get_json()
            
            # parse to the correct format
            dscvr_data = discovr.parse_json_convert_time(dscvr_data)
            dscvr_data = discovr.parse_json_prune(dscvr_data)
            
            w_dens = discovr.plasma_density(dscvr_data)
            w_spd = discovr.plasma_speed(dscvr_data)
            
            # create the final string to save to the logfile
            datastring = str(nowtime) + "," + str(coverage) + "," + str(w_spd) + "," + str(w_dens)
            print(datastring)
            
            log_data(datastring)
        except:
            print("Cannot log DISCOVR data")
        # #################################################################################
        # We need to implement the "predicting" algorith to forcast CH HSS impact, and even offer
        # possible future carrington rotations
        # #################################################################################
        
        # Pause for an hour
        time.sleep(3600)
           
