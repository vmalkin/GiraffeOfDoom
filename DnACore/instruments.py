"""
we will use abstraction to eal with instruments that offer the same data but have differing access methods
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
    """child class of instrument"""
    def __init__(self, name, location, owner):
        Instrument.__init__(self, name, location, owner)

    def print_output(self):
        print("This is a magnetometer")

