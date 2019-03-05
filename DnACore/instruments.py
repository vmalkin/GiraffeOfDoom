"""
Instrumentation. This file contains  parent/child objects to deal with the getting data from instrumentation
in multiple ways. Instrument is the abstract class. Each child class is contains the unique methods for getting
data from each different kind of device eg: local file, http, COM port, etc.
"""
import constants as k
import logging
import os
import datetime,time

errorloglevel = logging.DEBUG
logging.basicConfig(filename=k.errorfile, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")

class Datapoint:
    def __init__(self, posix_time, data):
        self.posix_time = posix_time
        self.data = data

    def print_values(self):
        returnstring = self.posix_time + "," + self.data
        return returnstring


class Instrument:
    """Abstract Class of instrument"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        self.name = name
        self.location = location
        self.owner = owner
        self.date_regex_string = date_regex_string
        self.datasource = datasource

        self.logfile_dir = self.name + "_logfiles"
        self.running_array_savefile = self.name + ".csv"

        self.load_dynamic_parameters()
        self.runningarray = self.running_array_load(self.running_array_savefile)
        self.setup_paths()

    def setup_paths(self):
        # setup file paths
        # Set up file structure for Data logs. Linux systems might need use of the mode arg to set correct permissions.
        if not os.path.exists(self.logfile_dir):
            try:
                os.makedirs(self.logfile_dir)
                print("Logfile directory created.")
            except:
                if not os.path.isdir(self.logfile_dir):
                    print("Unable to create log directory")
                    logging.critical("CRITICAL ERROR: Unable to create logs directory")

    def running_array_load(self, savefile):
        returnarray = []
        if os.path.exists(savefile):
            with open(savefile, "r") as s:
                for line in s:
                    line = line.strip()
                    line = line.split(",")
                    dp = Datapoint(line[0], line[1])
                    returnarray.append(dp)
                logging.debug("Running array loaded for " + self.name)
        return returnarray

    def running_array_save(self, runningarray):
        with open(self.running_array_savefile, "w") as w:
            for data_point in runningarray:
                w.write(data_point.print_values() + "\n")

    def utc_2_posic(self, utctime, dateformat, regex):
        # set date time format for strptime()
        # dateformat = "%Y-%m-%d %H:%M:%S.%f"
        # dateformat = '"%Y-%m-%d %H:%M:%S"'
        # dateformat = '%Y-%m-%d %H:%M'
        posixtime = datetime.strptime(utctime, dateformat)
        posixtime = time.mktime(posixtime.timetuple())
        return str(int(posixtime))

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
        pass

    def append_new_data(self):
        """Aggregate to internal list"""
        pass

    def prune_current_data(self):
        """Prune off the oldest entries - last 24 hours"""
        pass

    def save_logfile(self):
        """Save the current data to CSV logfile"""
        pass

    def process_data(self):
        """Wrapper function to process this instruments data gathering and parameter updating"""
        raise NotImplementedError


class MagnetometerLocalCSV(Instrument):
    """Child class of Instrument"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        Instrument.__init__(self, name, location, owner, date_regex_string, datasource)

    def process_data(self):
        print("Processing local magnetometer")


class MagnetometerGOES(Instrument):
    """Child class of Instrument - GOES satellite data from URL"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        Instrument.__init__(self, name, location, owner, date_regex_string, datasource)

    def process_data(self):
        print("Processing GOES satellite magnetometer")


class MagnetometerURL(Instrument):
    """Child class of Instrument - data from URL"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        Instrument.__init__(self, name, location, owner, date_regex_string, datasource)

    def process_data(self):
        print("Processing URL data")
