import mgr_data
import mgr_files
import mgr_serialport
import mgr_graph_simple
import mgr_dhdt
import mgr_binner
import datapoint
import time
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
                grapher_simple.wrapper_function()
            except:
                print("Simple grapher failed")
                logging.error("Simple grapher failed")
            
            # CReate the one-minute bin file for data fusion/display
            try:
                shortbins.processbins()
            except:
                print("1 min bins grapher failed")
                logging.error("1 min bins grapher failed")

            # Create the dH/dt display data
            try:
                mgr_dhdt.process_differences(datamanager.data_array)
            except:
                print("dH/dt processor failed")
                logging.error("dH/dt processor failed")

if __name__ == "__main__":
    print("Pything Data Logger")
    print("(c) Vaughn Malkin, 2015 - 2018")
    print("Version " + __version__)

    comport = mgr_serialport.SerialManager(k.portName,k.baudrate,k.bytesize,k.parity,k.stopbits,k.timeout,k.xonxoff,k.rtscts,k.writeTimeout,k.dsrdtr,k.interCharTimeout)
    filemanager = mgr_files.FileManager()
    datamanager = mgr_data.DataList()
    grapher_simple = mgr_graph_simple.Grapher(k.mag_read_freq, k.mag_running_count, k.field_correction, k.station_id, datamanager.data_array)
    shortbins = mgr_binner.Binner(datamanager.data_array, 86400, 60, k.field_correction)

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