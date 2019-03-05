"""
Instrumentation. This file contains  parent/child objects to deal with the getting data from instrumentation
in multiple ways. Instrument is the abstract class. Each child class is contains the unique methods for getting
data from each different kind of device eg: local file, http, COM port, etc.
"""
import constants as k
import logging, os, datetime, time

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
        self.array24hr_savefile = self.name + ".csv"

        self.array24hr = self.array24hr_load(self.array24hr_savefile)
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

    def array24hr_load(self, savefile):
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

    def array24hr_save(self):
        with open(self.array24hr_savefile, "w") as w:
            for data_point in self.array24hr:
                w.write(data_point.print_values() + "\n")

    def utc_2_posic(self, utctime, dateformat, regex):
        # set date time format for strptime()
        # dateformat = "%Y-%m-%d %H:%M:%S.%f"
        # dateformat = '"%Y-%m-%d %H:%M:%S"'
        # dateformat = '%Y-%m-%d %H:%M'
        posixtime = datetime.datetime.strptime(utctime, dateformat)
        posixtime = time.mktime(posixtime.timetuple())
        return str(int(posixtime))

    def get_data(self):
        """load current data"""
        raise NotImplementedError

    def array24hr_prune(self, array24hr):
        """Prune off the oldest entries - last 24 hours"""
        returnarray = []
        cutoffdate = int(time.time()) - (60*60*24)
        for dp in array24hr:
            if dp.posix_time > cutoffdate:
                returnarray.append(dp)
        return returnarray

    def convert_data(self):
        pass

    def append_raw_data(self, rawdata):
        pass

    def parse_dates(self, dpdata, dateregex):
        pass

    def save_logfile(self):
        """Save the current data to CSV logfile"""
        pass

    def process_data(self):
        """Wrapper function to process this instruments data gathering and parameter updating"""
        raise NotImplementedError


class MagnetometerWebCSV(Instrument):
    """Child class of Instrument - data from URL"""
    def __init__(self, name, location, owner, date_regex_string, datasource):
        Instrument.__init__(self, name, location, owner, date_regex_string, datasource)

    def get_data(self):
        pass

    def process_data(self):
        raw_data = self.get_data()
        dp_data = self.convert_data(raw_data)
        dp_data = self.parse_dates(dp_data, self.date_regex_string)

        self.array24hr = self.append_raw_data(dp_data)
        self.array24hr = self.array24hr_prune(self.array24hr)
        self.array24hr_save()
        self.save_logfile()

