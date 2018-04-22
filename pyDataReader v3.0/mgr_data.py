import time
import os
import logging
import re
errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)


# #############################
# D A T A P O I N T   C L A S S 
# #############################
class DataPoint:
    def __init__(self, posix_time, data_1):
        self.posix_time = posix_time
        self.data_1 = data_1
        
    # convert the internal posx_date to UTC format
    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posix_time)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        return utctime
    
    # create a string of labels
    def print_labels(self):
        return "Date/Time, Data value 1"

    # return the values of this datapoint as a astring
    def print_values(self, value_type):
        if value_type == "utc":
            return_time = self._posix2utc()
            return str(return_time) + "," + str(self.data_1)
        else:
            return str(self.posix_time) + "," + str(self.data_1)


# ###########################
# D A T A L I S T   C L A S S
# a datalist is a list of datapoints
# This class can manage the list
# ###########################
class DataList:
    def __init__(self):
        self._savefile = "arraysave.csv"
        self.data_array = self.list_load()

    # save the datapoint list to file
    def list_save(self):
        # export array to array-save file
        try:
            with open(self._savefile, 'w') as w:
                for dataObjects in self.data_array:
                    w.write(dataObjects.print_values("posix") + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + self._savefile)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + self._savefile)
    
    # load the data_array  of datapoints from the savefile
    def list_load(self):
        readings = []
        # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
        if os.path.isfile(self._savefile):
            with open(self._savefile) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    values = line.split(",")
                    # See the datapoint object/constructor for the current values it holds.
                    dp = DataPoint(values[0], values[1])
                    readings.append(dp)
            print("Array loaded from file. Size: " + str(len(readings)) + " records")
        else:
            print("No save file loaded. Using new array.")

        return readings
    
    # Append a new datapoint and prune the length of the data_array
    # if required. 
    def list_append(self, data_point, MAG_READ_FREQ):
        # Append the datapoint to the array. Prune off the old datapoint if the array is 24hr long

        if (len(self.data_array) < MAG_READ_FREQ * 60 * 24):
            self.data_array.append(data_point)
        else:
            self.data_array.pop(0)
            self.data_array.append(data_point)
