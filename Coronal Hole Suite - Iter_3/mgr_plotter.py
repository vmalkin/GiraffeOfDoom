"""
This py manages the plotting of values. It allows me to easily build up a CSV or other file that has
multiple series in it for use in APIS like Highcharts, etc.
"""
import time
import mgr_data
import os
import logging

READING_PREDICTED = "predictions.csv"
READING_ACTUAL = "log.csv"

class PlotPoint:
    def __init__(self):
        self.utcdate = ""
        self.series1value = 0
        self.series2value = 0

    def printvalues(self):
        value = str(self.utcdate) + "," + str(self.series1value) + "," + str(self.series2value)
        return value

# Class to manage the creation of CSV data with multiple values in it.
class Plotter:
    def __init__(self, finish_date ):
        self.null = ""
        self.reading_actual = self._load_csv_posixdates(READING_ACTUAL)
        self.reading_predicted = self._load_csv_posixdates(READING_PREDICTED)
        self.plotlist = []

    # load a CSV file and extract the dates only
    def _load_csv_date_data(self, filename):
        # returns an array loaded from the logfile.
        # list in format posix_date, ch_value, windspeed, winddensity
        logging.debug("loading datapoints from CSV: " + filename)
        returnlist = []
        with open (filename, 'r') as f:
            for line in f:
                line = line.strip()  # remove \n from EOL
                returnlist.append(line)
        return returnlist

