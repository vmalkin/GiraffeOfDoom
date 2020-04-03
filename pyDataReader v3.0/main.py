import mgr_data
import mgr_files
import mgr_serialport
import mgr_grapher
import datapoint
import time
import math
import logging
import re
import sys
from threading import Thread
import constants as k

__version__ = "3.1"
errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

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
                templist = mgr_grapher.median_filter(datamanager.data_array)
                templist = mgr_grapher.recursive_filter(templist)

                binlist = mgr_grapher.BinBinlist(60, templist, k.publish_folder + "/dna_fgm1.csv")
                binlist.process_datalist()
                binlist.save_file()
            except:
                print("Simple grapher failed")
                logging.error("Simple grapher failed")


if __name__ == "__main__":
    print("Pything Data Logger")
    print("(c) Vaughn Malkin, 2015 - 2019")
    print("Version " + __version__)

    comport = mgr_serialport.SerialManager(k.portName,k.baudrate,k.bytesize,k.parity,k.stopbits,k.timeout,k.xonxoff,k.rtscts,k.writeTimeout,k.dsrdtr,k.interCharTimeout)
    filemanager = mgr_files.FileManager()
    datamanager = mgr_data.DataList()


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
            reading_time = math.floor(time.time())

            # create the datapoint. Print the values for the user.
            data_point = datapoint.DataPoint(reading_time, magnetometer_reading)
            print(data_point.print_values("utc"))

            # Append to the running list of readings. Save the list.
            datamanager.list_append(data_point, k.mag_read_freq)
            datamanager.list_save()

            # Save the 24 hour logfile.
            filemanager.save_daily_log(data_point)

        else:
            print("Garbage data from Magnetometer: " + magnetometer_reading)
            logging.warning("WARNING: Garbage data from Magnetometer: " + magnetometer_reading)
