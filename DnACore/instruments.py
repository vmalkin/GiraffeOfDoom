"""
Instrumentation. This file contains  parent/child objects to deal with the getting data from instrumentation
in multiple ways. Instrument is the abstract class. Each child class is contains the unique methods for getting
data from each different kind of device eg: local file, http, COM port, etc.
"""


class Instrument:
    """Abstract Class of instrument"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        self.name = name
        self.location = location
        self.owner = owner
        self.date_regex_string = date_regex_string
        self.datasource = datasource

        self.load_dynamic_parameters()

    def load_dynamic_parameters(self):
        """An instrument can load it's unique parameters"""
        pass

    def calculate_dynamic_parameters(self):
        """Calculate current values for unique instrument parameters"""
        pass

    def save_dynamic_parameters(self):
        """An instrument can save it's unique parameters"""
        pass

    def get_data(self):
        """load current data"""
        raise NotImplementedError

    def append_new_data(self):
        """Aggregate to internal list"""
        pass

    def prune_current_data(self):
        """Prune off the oldest entries - last 24 hours"""
        pass

    def save_logfile(self):
        """Save the current data to CSV logfile"""
        pass


class MagnetometerLocalCSV(Instrument):
    """Child class of Instrument"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        Instrument.__init__(self, name, location, owner, date_regex_string, datasource)

    def get_data(self):
        returnvalue = "Data from local CSV file"
        return returnvalue


class MagnetometerGOES(Instrument):
    """Child class of Instrument - GOES satellite data from URL"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        Instrument.__init__(self, name, location, owner, date_regex_string, datasource)

    def get_data(self):
        returnvalue = "Data from local the Internet"
        return returnvalue
