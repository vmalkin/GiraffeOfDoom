import mgr_data
import mgr_files
import mgr_serialport
import mgr_graphing
import time
import logging
import re

__version__ = "3.0"
errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

# Constants and other global variables required
MAG_READ_FREQ = 30         # how often the magnetometer sends data per minute
STATION_ID = "RuruRapid."

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com8' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = '/dev/ttyACM0'
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


if __name__ == "__main__":
    print("Pything Data Logger")
    print("(c) Vaughn Malkin, 2015 - 2018")
    print("Version " + __version__)

    comport = mgr_serialport.SerialManager(portName,baudrate,bytesize,parity,stopbits,timeout,xonxoff,rtscts,writeTimeout,dsrdtr,interCharTimeout)
    filemanager = mgr_files.FileManager()
    datamanager = mgr_data.DataList()
    grapher = mgr_graphing.Grapher()

    while True:
        # single data value from com port
        magnetometer_reading = comport.data_recieve()

        # Checking here.
        # r'\A-?\d+(\.\d+)?[,]-?\d+(\.\d+)?[,]-?\d+(\.\d+)?\Z'
        # example of 3-value regex...
        if re.match(r'-?\d+', magnetometer_reading):

            # get the current POSIX time
            reading_time = time.time()

            # create the datapoint. Print the values for the user.
            data_point = mgr_data.DataPoint(reading_time, magnetometer_reading)
            print(data_point.print_values("utc"))

            # Append to the running list of readings. Save the list.
            datamanager.list_append(data_point, MAG_READ_FREQ)
            datamanager.list_save()

            # Save the 24 hour logfile.
            filemanager.save_daily_log(data_point)

            # create the highchart display files.
            grapher.wrapper()

        else:
            print("Garbage data from Magnetometer: " + magnetometer_reading)
            logging.warning("WARNING: Garbage data from Magnetometer: " + magnetometer_reading)


