import mgr_data
import mgr_files
import mgr_serialport
import mgr_graph_simple
import mgr_dhdt
import time
import logging
import re
import sys
from threading import Thread

__version__ = "3.0"
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

mag_read_freq = 30   # how many readings per minute
mag_running_count = 6   # width of the window for running average
noise_spike = 2   # threshold for rate of change noise
field_correction = -1   # graph should go up, as H value increases
station_id = "Ruru_Rapid"   # ID of magnetometer station

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


# CHARTING FUNCTION AS A THREAD
class ChartThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="SimpleChartingThread")

    def run(self):
        time.sleep(120)
        grapher_simple.wrapper_function()


if __name__ == "__main__":
    print("Pything Data Logger")
    print("(c) Vaughn Malkin, 2015 - 2018")
    print("Version " + __version__)

    comport = mgr_serialport.SerialManager(portName,baudrate,bytesize,parity,stopbits,timeout,xonxoff,rtscts,writeTimeout,dsrdtr,interCharTimeout)
    filemanager = mgr_files.FileManager()
    datamanager = mgr_data.DataList()
    grapher_simple = mgr_graph_simple.Grapher(mag_read_freq, mag_running_count, noise_spike, field_correction, station_id, datamanager.data_array)
    grapher_dhdt = mgr_dhdt.Differencer()

    # Thread code to implement charting in a new thread.
    grapher_thread = ChartThread()
    try:
        grapher_thread.start()
    except:
        print("Unable to start Charting Thread")
        logging.critical("CRITICAL ERROR: Unable to shart Highcharts Thread")
        print(str(sys.exc_info()))

    #The program begins here
    while True:
        # single data value from com port
        magnetometer_reading = comport.data_recieve()

        # Checking magnetometer values against regex here.
        # r'\A-?\d+(\.\d+)?[,]-?\d+(\.\d+)?[,]-?\d+(\.\d+)?\Z'
        # example of 3-value regex...
        if re.match(r'-?\d+', magnetometer_reading):

            # get the current POSIX time
            reading_time = time.time()

            # create the datapoint. Print the values for the user.
            data_point = mgr_data.DataPoint(reading_time, magnetometer_reading)
            print(data_point.print_values("utc"))

            # Append to the running list of readings. Save the list.
            datamanager.list_append(data_point, mag_read_freq)
            datamanager.list_save()

            # Save the 24 hour logfile.
            filemanager.save_daily_log(data_point)

        else:
            print("Garbage data from Magnetometer: " + magnetometer_reading)
            logging.warning("WARNING: Garbage data from Magnetometer: " + magnetometer_reading)
