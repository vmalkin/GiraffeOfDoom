class Datapoint:
    def __init__(self, time, altitude, azimuth, snr):
        self.time = time
        self.altitude = altitude
        self.azimuth = azimuth
        self.snr = snr

class Satellite:
    def __init__(self):
        self.datalist = []

    def speak(self, name):
        print("I am " + str(name))
