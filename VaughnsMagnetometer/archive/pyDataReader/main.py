#!/usr/bin/python
import DataPoint
import constants as k
import ArrayManager as am
import serial
import datetime
import logging
import os
import pytz

__author__ = 'Vaughn Malkin'
__version__ = "0.6.0"


# *****************************************************************************************
# Prime any globals
# *****************************************************************************************

# *****************************************************************************************
# B E G I N   F U N C T I O N   D E F I N I T I O N S
# *****************************************************************************************

def CheckData(logDataToAdd):
    # Checking here. Regex.
    LogRawMagnetometerData(logDataToAdd)

# *****************************************************************************************
# FUNCTION - create a rotating log for data based on date
# *****************************************************************************************
def LogRawMagnetometerData(logDataToAdd):
    # get current datetime based on system clock. NOT UTC by default
    # dt = datetime.datetime.now()
    dt = datetime.datetime.utcnow()


    # LogdatatoAdd is 3 comma sep values
    lg = logDataToAdd.split(",")

    # Create the DataPoint object. Calculations are performed. DP is added to array.
    dp = DataPoint.DataPoint(str(dt), lg[0], lg[1], lg[2])
    am.AppendDataPoint(dp, readings)

    # Logdata to be appended to current 24 hr file
    logData = dp.dateTime + "," + dp.rawMagX + "," + dp.rawMagY + "," + dp.rawMagZ

    # RAW log file name is created now. Get the date part of dt, add file suffix
    RawlogName = str(dt.date())
    RawlogName = k.PATH_LOGS + RawlogName + '.csv'

    # If the logfile exists...
    if os.path.isfile(RawlogName):
        try:
            with open (RawlogName,'a') as f:
                f.write(logData + '\n')
        except IOError:
            print("WARNING: There was a problem accessing the current logfile: " + RawlogName)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + RawlogName)
        else:
            print("Data logged ok: ", logData + "  Array Size: " + str(len(readings)))

        # Save the RawArray
        am.SaveRawArray(readings)

        # create the output for the graphing logfiles
        am.CreateOutputFileArray(readings)

    # ELSE add the header to the file because it is new
    else:
        try:
            with open (RawlogName,'a') as f:
                f.write("DateTime (UTC), magX, magY, magZ" + '\n')

            print("Creating new logfile")
        except IOError:
            print("WARNING: There was a problem accessing the current logfile: " + RawlogName)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + RawlogName)


# *****************************************************************************************
# E N D   F U N C T I O N   D E F I N I T I O N S
# *****************************************************************************************


# *****************************************************************************************
# B E G I N   M A I N
# *****************************************************************************************

# Setup error/bug logging
logging.basicConfig(filename=k.FILE_ERRORLOG, format='%(asctime)s %(message)s')

# setup file paths
# Set up file structure for Data logs. Linux systems might need use of the mode arg to set correct permissions.
try:
    os.makedirs(k.PATH_LOGS)
    print("Logfile directory created.")
except:
    if not os.path.isdir(k.PATH_LOGS):
        print("Unable to create log directory")
        logging.critical("CRITICAL ERROR: Unable to create logs directory")
try:
    os.makedirs(k.PATH_GRAPHING)
    print("Graphing file directory created.")
except:
    if not os.path.isdir(k.PATH_LOGS):
        print("Unable to create Graphing file directory")
        logging.critical("CRITICAL ERROR: Unable to create Graphing file directory")

# setup array for datapoints
readings = []

# Set up the infernal com port. Add a TRY-CATCH to deal with possible com port problems
try:
    com = serial.Serial(k.portName,k.baudrate,k.bytesize,k.parity,k.stopbits,k.timeout,k.xonxoff,k.rtscts,k.writeTimeout,k.dsrdtr,k.interCharTimeout)
except serial.SerialException:
    print("CRITICAL ERROR: Com port not responding. Please check parameters")
    logging.critical("CRITICAL ERROR: Unable to open com port. Please check com port parameters and/or hardware!!")

# Print out the port name for the edification of all concerned
print("Port is: ", com.name)

# Initialise array from savefile if possible, otherwise new array
am.CreateRawArray(readings)

# *****************************************************************************************
# MAIN LOOP. Only the End of Days will stop this program.
# Actually we need some kind of timeout on this.
# *****************************************************************************************
while True:
    logData = com.readline()                    # logData is a byte array, not a string at this point
    logData = str(logData,'ascii').strip()      # convert the byte array to string. strip off unnecessary whitespace

    # We need some kind of logic depending on the result of the stringchecker test as to whether or not we upload to the database.
    CheckData(logData)

