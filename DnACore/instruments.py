"""
Instrumentation. This file contains  parent/child objects to deal with the getting data from instrumentation
in multiple ways. Instrument is the abstract class. Each child class is contains the unique methods for getting
data from each different kind of device eg: local file, http, COM port, etc.
"""


class Instrument:
    """THis is an Abstract Class of instrument"""
    def __init__(self, name, location, owner):
        self.name = name
        self.location = location
        self.owner = owner

    def load_dynamic_parameters(self):
        """An instrument can load it's unique parameters"""
        pass

    def save_dynamic_parameters(self):
        """An instrument can save it's unique parameters"""
        pass



class Magnetometer(Instrument):
    """A Magnetometer inherits properties/methods from the Instrument class"""
    def __init__(self, name, location, owner):
        Instrument.__init__(self, name, location, owner)

    def print_output(self):
        print("This is a magnetometer")

