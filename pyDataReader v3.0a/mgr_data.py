import os
import logging
import datapoint as dp

errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)



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
    
    # load the data_array  of datapoints from the savefile on initialisation of the data manager
    def list_load(self):
        readings = []
        # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
        if os.path.isfile(self._savefile):
            with open(self._savefile) as e:
                for line in e:
                    line = line.strip()  # remove any trailing whitespace chars like CR and NL
                    values = line.split(",")
                    # See the datapoint object/constructor for the current values it holds.
                    datap = dp.DataPoint(values[0], values[1])
                    readings.append(datap)
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
