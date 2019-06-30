"""
The Grapher class is used to create the output files for graphing on the web using an API like Hightcharts
We want tp smooth the raw data and produce files of custom duration
We also want to produce the Differences Graph, and flip the orientation of the chart so that increasing magnetic field
readings measn the grph goes up
"""
from decimal import Decimal
import os
import logging
import datapoint as dp
import constants as k

errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

class Grapher():
    def __init__(self, mag_read_freq, mag_running_count, field_correction, station_id, rawdata):
        self._mag_read_freq = mag_read_freq
        self._mag_running_count = mag_running_count
        self._field_correction = field_correction
        self._station_id = station_id
        self._rawdata = rawdata

    # #################################################################################
    # data inverter
    # If necessary, invert the data so that trends up mean increasing field strength
    # #################################################################################
    def _invert_data_array(self):
        returnarray = []
        for dataitem in self._rawdata:
            newdata = float(dataitem.data_1) * float(self._field_correction)
            newdp = dp.DataPoint(dataitem.posix_time, newdata)
            returnarray.append(newdp)

        return returnarray

    # #################################################################################
    # Create the smoothed data array and write out the files for plotting.
    # We will do a running average based on the running average time in minutes and the number
    # readings per minute
    #
    # we will divide this number evenly so our average represents the midpoint of these
    # readings.
    # #################################################################################
    def _running_average(self, input_array, averaging_interval):

        displayarray = []
        recursive_constant = 0.5

        # NOW average the cumulative array, smooth out the blips
        if len(input_array) > 20:
            prev_data = input_array[0].data_1
            for i in range(1, len(input_array)):
                newdata = (recursive_constant * input_array[i].data_1) + ((1 - recursive_constant) * prev_data)
                datap = dp.DataPoint(input_array[i].posix_time, newdata)
                displayarray.append(datap)
                prev_data = newdata
        else:
            displayarray = input_array

        return displayarray

    # ############################################################
    # Create display file for Highcharts
    # ############################################################
    def _create_hichart_datafile(self, readingsArray, splitvalue, filename):

        splitvalue = len(readingsArray) - splitvalue

        if splitvalue < 1:
            splitvalue = 0

        displayList = readingsArray[splitvalue:]
        # print(len(displayList))

        try:
            os.remove(filename)
        except OSError:
            print("WARNING: could not delete " + filename)
            logging.warning("WARNING: File IO Exception raised - could not delete: " + filename)

        try:
            with open(filename, 'a') as f:
                f.write("Date/Time (UTC), Reading" + "\n")
                for datapoints in displayList:
                    f.write(datapoints.print_values("utc") + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + filename)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + filename)

    # ############################################################
    # W R A P P E R   F U N C T I O N
    # ############################################################
    def wrapper_function(self):
        # correct sign of data so increasing values = incr mag field
        revised_data = self._invert_data_array()
        # smooth data slightly
        revised_data = self._running_average(revised_data, 6)

        # Create the CSV display files
        splitvalue = self._mag_read_freq * 60 * 1
        self._create_hichart_datafile(revised_data, splitvalue, k.publish_folder + "/" + k.station_id + "_60mins.csv")

        # to get the last 24 hours the split value is mag read frequency * 60 * 24
        splitvalue = self._mag_read_freq * 60 * 24
        self._create_hichart_datafile(revised_data, splitvalue, k.publish_folder + "/" + k.station_id + "_24hrs.csv")
