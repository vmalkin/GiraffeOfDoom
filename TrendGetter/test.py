import mgr_binner as binner
import os
import time

class DataPoint:
    def __init__(self, posix_time, data_1):
        self.posixdate = posix_time
        self.utc_time = self._posix2utc()
        self.data = data_1

    # convert the internal posx_date to UTC format
    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posixdate)))
        utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
        return utctime

    # create a string of labels
    def print_labels(self):
        return "Date/Time, Data value, POSIX timestamp"

    # return the values of this datapoint as a astring
    def print_values(self, value_type):
        printvalue = ""

        if value_type == "utc":
            printvalue = str(self.utc_time) + "," + str(self.data)

        elif value_type == "combined":
            printvalue = str(self.utc_time) + "," + str(self.posixdate) + "," + str(self.data)

        else:
            printvalue = str(self.posixdate) + "," + str(self.data)

        return printvalue

# load the data_array  of datapoints from the savefile
def list_load():
    readings = []
    _savefile = "arraysave.csv"
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(_savefile):
        with open(_savefile) as e:
            for line in e:
                line = line.strip()  # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                # See the datapoint object/constructor for the current values it holds.
                datap = DataPoint(values[0], values[1])
                readings.append(datap)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded. Using new array.")

    return readings

if __name__ == "__main__":
    # use a preloaded data array to create a station
    dataarray = list_load()

    station  = binner.Station("TEST", dataarray, "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d", "%Y-%m-%d %H:%M:%S.%f")
    station.process_data()