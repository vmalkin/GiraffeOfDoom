"""
This py manages the plotting of values. It allows me to easily build up a CSV or other file that has
multiple series in it for use in APIS like Highcharts, etc.
"""
import time
import mgr_data
import os
import logging

PLOTFILE = "predictions.csv"

# Class to manage the creation of CSV data with multiple values in it.
class plotpoint:
    def __init__(self, finish_date ):
        self.null = ""
        self.start_date = self.finish_date - 86400
        self.finish_date = finish_date   # POSIX datestamp
        self.reading_actual = self.null   # the actual reading
        self.reading_predicted = self.null  # the predicted reading


    # convert the internal posx_date to UTC format
    def posixdate(self):
        utctime = time.gmtime(int(float(self.start_date)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        return utctime

    def return_values_string(self):
        returnstring = str(self.posixdate()) + "," + str(self.reading_actual) + "," + str(self.reading_predicted)
        return returnstring


# generic script to write out a CSV file
def write_csv(array, file)  :
    with open(file, 'w') as w:
        for item in array:
            w.write(str(item) + '\n')

# load a CSV file and extract the dates only
def load_csv_posixdates(filename):
    # returns an array loaded from the logfile.
    # list in format posix_date, ch_value, windspeed, winddensity
    logging.debug("loading datapoints from CSV: " + filename)

    returnlist = []
    if os.path.isfile(filename):
        with open (filename, 'r') as f:
            for line in f:
                line = line.strip()  # remove \n from EOL
                datasplit = line.split(",")
                posixdate = datasplit[0]   # our date should always be the 0-th value
                returnlist.append(posixdate)
    return returnlist





def create_plotfile(readingslist_actual, readingslist_predicted):
    # create the list of datapoints, using both lists as appropriate. We need to carefull manage the start and
    # finish times for each datapoint as these will be used to bin the data.
    actual = load_csv_posixdates("log.csv")
    predicted = load_csv_posixdates("prediction.csv")

    startdate = actual[0]
    enddate = predicted[len(predicted) - 1]

    returnlist = []
    returnlist.append(startdate)
    returnlist.append(enddate)


    # Load the saved CSV data, both actual readings and predicted values into lists

    # Build up the display array with the posix_time buckets

    # add the valuestring from each datapoint into the appropriate posix_time bucket in the list

    # write out to csv