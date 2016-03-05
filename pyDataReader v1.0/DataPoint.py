# Datapoint class
__author__ = 'vaughn'

class DataPoint:
    def __init__(self, dateTime, raw_x, raw_y, raw_z, raw_diff_x = 0, raw_diff_y = 0, raw_diff_z = 0):
        self.dateTime = dateTime
        self.raw_x = raw_x
        self.raw_y = raw_y
        self.raw_z = raw_z

        self.raw_diff_x = raw_diff_x
        self.raw_diff_y = raw_diff_y
        self.raw_diff_z = raw_diff_z

    def print_labels(self):
        return "Date/Time (UTC), Raw X, Raw Y, Raw Z, X Diffs, Y Diffs, Z Diffs"

    def print_values(self):
        return self.dateTime + "," + str(self.raw_x) + "," + str(self.raw_y) + "," + str(self.raw_z) + "," + \
               str(self.raw_diff_x) + "," + str(self.raw_diff_y) + "," + str(self.raw_diff_z)