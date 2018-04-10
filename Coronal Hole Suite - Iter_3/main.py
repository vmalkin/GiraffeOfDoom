import datetime
import parse_discovr_data as discovr
import mgr_solar_image as solar
import forecast
import urllib.request
import time
import logging
import mgr_data as dp
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
def save_display_file(datapoint_list, filename):
    returndata = []
    for item in datapoint_list:
        dataitem = str(item._posix2utc()) + "," + str(item.coronal_hole_coverage) + "," + str(item.wind_speed) + "," + str(item.wind_density)
        returndata.append(dataitem)
    with open (filename, 'w') as w:
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
    logging.debug("starting image from URL download: " + filename)
    try:
        request = urllib.request.Request(imageurl, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout = 10)
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
        save_display_file(datalist, "display.csv")

        print(newdatapoint.return_values() + "  (" + newdatapoint._posix2utc() + " UTC)")

        # #################################################################################
        # We need to implement the "predicting" algorith to forcast CH HSS impact, and even offer
        # possible future carrington rotations
        # #################################################################################

        # determine if we have enough data to begin a regression analysis. seeing as transit time is
        # approx 4 days, lets choose 8 days before we start predicting...
        WAITPERIOD = 86400 * 5
        startdate = datalist[0].posix_date
        nowdate = datalist[len(datalist) - 1].posix_date
        elapsedtime = nowdate - startdate
        timeleft = (WAITPERIOD - elapsedtime) / (60*60*24)

        if elapsedtime >= WAITPERIOD:
            forecast.calculate_forecast(datalist)
        else:
            # getcontext().prec = 4
            # timeleft = Decimal(timeleft)
            print("Insufficient time has passed to begin forecasting. " + str(timeleft)[:5] + " days remaining")

        # Pause for an hour
        time.sleep(3600)
