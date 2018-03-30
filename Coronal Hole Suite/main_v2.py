import datetime
import parse_discovr_data as discovr
import parse_solar_image as solar
import forecast
import urllib.request
import time

WIND_SPEED_THRESHOLD = 800
LOGFILE = 'log.csv'
__version__ = '0.2'

def load_data(filename):
    # returns an array loaded from the logfile. 
    returnlist = []
    try:
        with open (filename, 'r') as f:
            for line in f:
                line = line.strip()  # remove \n from EOL
                returnlist.append(line)
    except:
        print("No logfile. Starting from scratch")
    return returnlist

def save_data(datalist, filename):
    # Save a list to a disc file
    with open (filename, 'w') as w:
        for item in datalist:
            w.write(str(item) + '\n')
    
def prune_datalist(datalist):
    # Keep the datalist 3 carrington rotations long
    return datalist

#def log_data(value_string):
#    # If the logfile exists append the datapoint
#    try:
#        with open (LOGFILE,'a') as f:
#            f.write(value_string + '\n')
#            # print("Data logged ok. Array Size: " + str(len(readings)))
#    except IOError:
#        print("WARNING: There was a problem accessing the current logfile: " + LOGFILE)
    
def get_utc_time():
    # returns a STRING of the current UTC time
    time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    return time_now


 # #################################################################################
 # B E G I N   M A I N   H E R E 
 # #################################################################################  
print("Empirical Space Weather Forecast Tool")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("As based on:")
print("http://oh.geof.unizg.hr/SOLSTEL/images/dissemination/papers/Rotter2015_SoPh290_arxiv.pdf")
print("http://swe.uni-graz.at/index.php/services/solar-wind-forecast")
print("Code Implementation (c) 2018, Vaughn Malkin\n\n")
if __name__ == '__main__':
    # load up the main datalist
    datalist = load_data(LOGFILE)
    
    # make a oneoff backup at loadtime. 
    save_data(datalist, 'log.backup')

    while True:   
        try:
            # open an image
            # Grab the SWPS Syntopic Map for Local Display
            URL = 'https://services.swpc.noaa.gov/images/synoptic-map.jpg'
            
            with urllib.request.urlopen(URL) as url:
                with open('syntopic.jpg', 'wb') as f:
                    f.write(url.read())
            
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
        datastring = ""
        dscvr_data = discovr.get_json()
        
        if dscvr_data == "no_data":
            # Unable to get DISCOVR data
            datastring = str(nowtime) + "," + str(coverage) + ",0,0,0"
        else:        
            # parse to the correct format
            # The timestampt is in POSIX format
            dscvr_data = discovr.parse_json_convert_time(dscvr_data)
            dscvr_data = discovr.parse_json_prune(dscvr_data)
            
            w_dens = discovr.plasma_density(dscvr_data)
            w_spd = discovr.plasma_speed(dscvr_data)
            
            # High wind speeds may be due to CME and not teh High Speed Stream
            # set the wind speed value to NUL of this is the case. 
            if w_spd >= WIND_SPEED_THRESHOLD:
                w_spd = 0
            
            # create the final string to save to the logfile
            datastring = str(nowtime) + "," + str(coverage) + "," + str(w_spd) + "," + str(w_dens)
            
        # Append to the datalist
        datalist.append(datastring)    
        
        # Prune the datalist to be 3 Carrington Rotations long
        datalist = prune_datalist(datalist)
        
        # Save the datalist to file, display output.
        save_data(datalist, LOGFILE)
        print(datastring)

        # #################################################################################
        # We need to implement the "predicting" algorith to forcast CH HSS impact, and even offer
        # possible future carrington rotations
        # #################################################################################
        
        # Pause for an hour
        time.sleep(3600)
       
