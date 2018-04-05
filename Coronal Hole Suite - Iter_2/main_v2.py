import datetime
import parse_discovr_data as discovr
import parse_solar_image as solar
import forecast
import urllib.request
import time
import logging
import datapoint as dp
import os

# setup error logging
# logging levels in order of severity:
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

WIND_SPEED_THRESHOLD = 800
LOGFILE = 'log.csv'
DISPLAYFILE = 'display.csv'
CARRINGTON_ROTATION = 655   # hours
__version__ = '0.8'

# load a CSV file into a list
def load_datapoints(filename):
    # returns an array loaded from the logfile.
    # list in format posix_date, ch_value, windspeed, winddensity
    logging.debug("loading datapoints from CSV: " + filename)

    returnlist = []
    if os.path.isfile(filename):
        with open (filename, 'r') as f:
            for line in f:
                line = line.strip()  # remove \n from EOL
                datasplit = line.split(",")
                posixdate = datasplit[0]
                ch = datasplit[1]
                speed = datasplit[2]
                density = datasplit[3]
                dataitem = dp.DataPoint(posixdate, ch, speed, density)
                # logging.debug(posixdate + " " + ch + " " + speed + " " + density)
                returnlist.append(dataitem)
    else:
        print("No logfile. Starting from scratch")
    return returnlist

# Save a list ot a CSV data file
def save_csv(csvlist, filename):
    # Save a list to a disc file
    # list in format posix_date, ch_value, windspeed, winddensity
    with open (filename, 'w') as w:
        for item in csvlist:
            w.write(str(item) + '\n')

# save datapoint list
def save_datapoint(datapoint_list, filename):
    # list in format posix_date, ch_value, windspeed, winddensity
    logging.debug("SAVING datapoint values to file: " + filename)
    with open(filename, 'w') as f:
        for dpoint in datapoint_list:
            f.write(dpoint.return_values() + '\n')


# Save list to CSV - convert posix time in list to UTC
def save_display_file(datalist):
    returndata = []

    for item in datalist:
        datasplit = item.split(",")
        timestamp = datasplit[0]
        # utctime = datetime.datetime.fromtimestamp(int(float(timestamp))).strftime('%Y-%m-%d %H:%M:%S')
        utctime = time.gmtime(int(float(timestamp)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        dataitem = (utctime) + "," + datasplit[1] + "," + datasplit[2] + "," + datasplit[3]

        returndata.append(dataitem)

    with open (DISPLAYFILE, 'w') as w:
        for item in returndata:
            w.write(str(item) + '\n')

# Prune the size of the datalist
def prune_datalist(datalist):
    # Keep the datalist 3 carrington rotations long
    listlength = (CARRINGTON_ROTATION * 3)
    returnlist = []

    if len(datalist) > listlength:
        chop = len(datalist) - listlength
        returnlist = datalist[chop:]
    else:
        returnlist = datalist

    return returnlist

def get_utc_time():
    # returns a STRING of the current UTC time
    time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    return time_now

def get_posix_time():
    time_now = time.time()
    return time_now

def save_image_from_url(imageurl, filename):
    logging.debug("starting image from URL download")
    try:
        request = urllib.request.Request(imageurl, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request)
        with open(filename, 'wb') as f:
            f.write(response.read())
    except urllib.request.HTTPError:
        logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))

 # #################################################################################
 # B E G I N   M A I N   H E R E 
 # #################################################################################  
print("\nEmpirical Space Weather Forecast Tool")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("As based on:")
print("http://oh.geof.unizg.hr/SOLSTEL/images/dissemination/papers/Rotter2015_SoPh290_arxiv.pdf")
print("http://swe.uni-graz.at/index.php/services/solar-wind-forecast")
print("Code Implementation (c) 2018, Vaughn Malkin\n\n")
if __name__ == '__main__':
    # load up the main datalist
    datalist = load_datapoints(LOGFILE)
    
    # make a oneoff backup at loadtime. 
    save_datapoint(datalist, 'log.backup')

    while True:
        # open an image
        # Grab the SWPS Syntopic Map for Local Display
        save_image_from_url('https://services.swpc.noaa.gov/images/synoptic-map.jpg', 'syntopic.jpg')

        try:
            save_image_from_url("https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg", "sun.jpg")

            img = solar.image_read('sun.jpg')

            #current UTC time
            # nowtime_utc = get_utc_time()
            nowtime_posix = get_posix_time()

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

            # Full disk image
            outputimg1 = solar.mask_img(outputimg, mask1)
            solar.add_img_logo(outputimg1)
            solar.image_write('disc_full.bmp', outputimg1)

            # Meridian Segment
            outputimg2 = solar.mask_img(outputimg, mask2)
            solar.image_write('disc_segment.bmp', outputimg2)

            # Calculate the area occupied by coronal holes
            coverage = solar.count_pixels(outputimg2, mask2)
        except:
            logging.error("Unable to process SDO image")

        # #################################################################################
        # Get the DISCOVR solar wind data (speed and density)
        # We do need to check that data is timely!! Naive implementation at the moment
        # #################################################################################
        datastring = ""
        dscvr_data = discovr.get_json()

        if dscvr_data == "no_data":
            # Unable to get DISCOVR data
            # datastring = str(nowtime_posix) + "," + str(coverage) + ",0,0"
            newdatapoint = dp.DataPoint(nowtime_posix, coverage, 0, 0)
        else:
            # parse new data to the correct format
            # The timestampt is in POSIX format
            dscvr_data = discovr.parse_json_convert_time(dscvr_data)

            # we want only the ast hour of data
            dscvr_data = discovr.parse_json_prune(dscvr_data)

            # get the avg windspeed and plasma density
            w_dens = discovr.plasma_density(dscvr_data)
            w_spd = discovr.plasma_speed(dscvr_data)

            # High wind speeds may be due to CME and not teh High Speed Stream
            # set the wind speed value to NUL of this is the case.
            if (w_spd) >= WIND_SPEED_THRESHOLD:
                w_spd = 0

            # create the final string to save to the logfile
            # datastring = str(nowtime_posix) + "," + str(coverage) + "," + str(w_spd) + "," + str(w_dens)
            newdatapoint = dp.DataPoint(nowtime_posix, coverage, w_spd, w_dens)

        # Append to the datalist
        datalist.append(newdatapoint)

        # Prune the datalist to be 3 Carrington Rotations long
        datalist = prune_datalist(datalist)

        # Save the datalist to file. CReate the display file. Print output to console
        # for thing in datalist:
        #     print(thing.return_values())

        save_datapoint(datalist, LOGFILE)
        save_datapoint(datalist, "display.csv")

        print(newdatapoint.return_values() + "  (" + get_utc_time() + " UTC)")

        # #################################################################################
        # We need to implement the "predicting" algorith to forcast CH HSS impact, and even offer
        # possible future carrington rotations
        # #################################################################################
        forecast.calculate_forecast(datalist)

        # Pause for an hour
        time.sleep(3600)
   
