import math
class Datapoint:
    def __init__(self, time, altitude, azimuth, snr):
        self.time = time
        self.altitude = altitude
        self.azimuth = azimuth
        self.snr = snr
        self.i_value = math.pow(10, (snr/10))

class Satellite:
    def __init__(self):
        self.datalist = []

