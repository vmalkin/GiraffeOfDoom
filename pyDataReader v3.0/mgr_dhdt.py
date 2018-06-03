import time

class DisplayPoint():
    def __init(self):
        self.datavalue
        self.high_value
        self.low_value
        self.posix_time
        
    def _posix2utc(self):
        utctime = time.gmtime(int(float(self.posix_time)))
        utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
        return utctime

    def print_values(self):
        value_string = (str(self._posix2utc()) + "," + str(self.average_value() * self._flipvalue))
        return value_string

