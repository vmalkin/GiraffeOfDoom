# Datapoint class
import DataPoint
import math
__author__ = 'vaughn'

dateTime = ""       # Datetime of reading
rawMagX = 0         # the actual data reading
rawMagY = 0         # the actual data reading
rawMagZ = 0         # the actual data reading


class DataPoint:
    def __init__(self, dateTime, rawMagX, rawMagY, rawMagZ):
        self.dateTime = dateTime
        self.rawMagX = rawMagX
        self.rawMagY = rawMagY
        self.rawMagZ = rawMagZ
