import time
__author__ = 'vaughn'

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
            return_time = self._posix2utc(self.posix_time)
            return str(return_time) + "," + str(self.data_1)
        else:
            return self.posix_time + "," + str(self.data_1)


# ###########################
# D A T A L I S T   C L A S S
# a datalist is a list of datapoints
# This class can manage the list
# ###########################
class DataList:
    def __init__ (self):
        self._savefile = "arraysave.csv"
        self.data_array = self.list_load()
    
    # save the datapoint list to file
    def list_save(self):
        pass
    
    # load the data_array  of datapoints from the savefile
    def list_load(self):
        pass
    
    # Append a new datapoint and prune the length of the data_array
    # if required. 
    def list_append(self, data_point):
        pass
    
    