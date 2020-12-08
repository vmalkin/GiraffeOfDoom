import serial
import time
import logging
import re
import sys
from threading import Thread
import constants as k

__version__ = "4.0"
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)
comport_regex = r'^(\d{3} \d{6}[ ?]\d{6})$'
station_id = "ruru"   # ID of magnetometer station

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com41'  # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = '/dev/ttyUSB0'
baudrate = 9600
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 60
xonxoff = False
rtscts = True
writeTimeout = None
dsrdtr = False
interCharTimeout = None


# CHARTING FUNCTION AS A THREAD
class ChartThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="SimpleChartingThread")
        print("Starting thread for charting")

    def run(self):
        while True:
            time.sleep(60)
            # create the CSV files for general display
            print("Create Highcharts")
            try:
                pass
            except:
                print("Simple grapher failed")
                logging.error("Simple grapher failed")


class SerialManager():
    def __init__(self, portName,baudrate,bytesize,parity,stopbits,timeout,xonxoff,rtscts,writeTimeout,dsrdtr,interCharTimeout):
        self._portName = portName
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self._xonxoff = xonxoff
        self._rtscts = rtscts
        self._writeTimeout = writeTimeout
        self._dsrdtr = dsrdtr
        self._interCharTimeout = interCharTimeout

        try:
            self.com = serial(self._portName, self._baudrate, self._bytesize, self._parity, self._stopbits, self._timeout, self._xonxoff,
                                self._rtscts, self._writeTimeout, self._dsrdtr, self._interCharTimeout)
        except serial.SerialException:
            print("CRITICAL ERROR: Com port not responding. Please check parameters")
            logging.critical("CRITICAL ERROR: Unable to open com port. Please check com port parameters and/or hardware!!")
            print("\n\n" + str(sys.exc_info()))

    def data_recieve(self):
        logData = self.com.readline()  # logData is a byte array, not a string at this point
        logData = str(logData, 'ascii').strip()  # convert the byte array to string. strip off unnecessary whitespace
        return logData


if __name__ == "__main__":
    print("Pything Data Logger")
    print("(c) Vaughn Malkin, 2015 - 2021")
    print("Version " + __version__)

    comport = SerialManager(portName, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, writeTimeout, dsrdtr, interCharTimeout)

    # Thread code to implement charting in a new thread.
    grapher_thread = ChartThread()
    try:
        grapher_thread.start()
    except:
        print("Unable to start Charting Thread")
        logging.critical("CRITICAL ERROR: Unable to shart Highcharts Thread")
        print(str(sys.exc_info()))

    # The program begins here
    while True:
        # single data value from com port
        magnetometer_reading = comport.data_recieve()

        if re.match(comport_regex, magnetometer_reading):
            pass
            # get the current POSIX time
            # create the datapoint. Print the values for the user.
            # Append to the running list of readings. Save the list.
            # Save the 24 hour logfile.

        else:
            print("Garbage data from Magnetometer: " + magnetometer_reading)
            logging.warning("WARNING: Garbage data from Magnetometer: " + magnetometer_reading)
