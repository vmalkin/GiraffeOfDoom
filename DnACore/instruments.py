"""
Instrumentation. This file contains  parent/child objects to deal with the getting data from instrumentation
in multiple ways. Instrument is the abstract class. Each child class is contains the unique methods for getting
data from each different kind of device eg: local file, http, COM port, etc.
"""
import constants as k
import logging
import os
import datetime, time
import requests
import re
import calendar

errorloglevel = logging.WARNING
logging.basicConfig(filename=k.errorfile, format='%(asctime)s %(message)s', level=errorloglevel)
logging.info("Created error log for this session")


class Datapoint:
    def __init__(self, posix_time, data):
        self.posix_time = posix_time
        self.data = data

    def posix2utc(self, posixvalue):
        # utctime = datetime.datetime.fromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        utctime = datetime.datetime.utcfromtimestamp(int(posixvalue)).strftime('%Y-%m-%d %H:%M:%S')
        return utctime

    def print_values_posix(self):
        returnstring = str(self.posix_time) + "," + str(self.data)
        return returnstring

    def print_values_utc(self):
        timestamp = self.posix2utc(self.posix_time)
        returnstring = str(timestamp) + "," + str(self.data)
        return returnstring


class Instrument:
    """Abstract Class of instrument"""
    def __init__(self, name, location, owner, dt_regex, dt_format, datasource):
        self.name = name
        self.location = location
        self.owner = owner
        self.dt_regex = dt_regex
        self.dt_format = dt_format
        self.datasource = datasource

        self.logfile_dir = self.name + "_raw_logs"
        self.array24hr_savefile = self.name + ".csv"
        self.headers = {}
        self.headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"

        self.array24hr = self.array24hr_load(self.array24hr_savefile)
        self.setup_paths()

    def setup_paths(self):
        """Set up needed file paths"""
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
        """load the 24hr running array"""
        returnarray = []
        if os.path.exists(savefile):
            print("loading data for " + self.name)
            with open(savefile, "r") as s:
                for line in s:
                    line = line.strip()
                    line = line.split(",")
                    dp = Datapoint(line[0], line[1])
                    returnarray.append(dp)
                logging.debug("Running array loaded for " + self.name)
        print(str(len(returnarray)) + " values loaded")
        return returnarray

    def array24hr_save(self):
        """Save the 24hr running array"""
        try:
            with open(self.array24hr_savefile, "w") as w:
                for data_point in self.array24hr:
                    w.write(data_point.print_values_posix() + "\n")
        except PermissionError:
            logging.critical("CRITICAL: Unable to save 24 hr running array for " + str(self.name))

    def get_raw_data(self):
        """load current data from original source. Should return a string "NULL" if getting fails"""
        raise NotImplementedError

    def parse_raw_data(self, rawdata):
        """Converts raw data into a array with [date, data] layout.
           If parsing FAILS we should abort the rest of the processing.
        """
        raise NotImplementedError

    def array24hr_prune(self, array24hr):
        """Prune off the oldest entries - last 24 hours"""
        returnarray = []
        cutoffdate = int(time.time()) - (60*60*24)
        # print(datetime.datetime.utcfromtimestamp(int(cutoffdate)).strftime('%Y-%m-%d %H:%M:%S'))
        for dp in array24hr:
            if int(dp.posix_time) > cutoffdate:
                returnarray.append(dp)
        return returnarray

    def convert_data(self, rawdata, datetime_regex):
        """Convert CSV or JSON data to datapoint objects"""
        object_list = []
        try:
            for item in rawdata:
                item = item.split(",")
                if re.match(datetime_regex, item[0]):
                    date_obj = datetime.datetime.strptime(item[0], self.dt_format)
                    posixtime = calendar.timegm(date_obj.timetuple())
                    dp = Datapoint(posixtime, item[1])
                    object_list.append(dp)
        except:
            logging.warning("WARNING: Appears to be no data for " + str(self.name) + ". Ubnable to convert timestamps.")
        return object_list

    def append_raw_data(self, rawdata):
        """Appends data newer than the most recent datetime in the 24hr array"""
        most_recent_index = len(self.array24hr) - 1

        if most_recent_index > 0:
            most_recent_datapoint = self.array24hr[most_recent_index]
            for dpobject in rawdata:
                if int(dpobject.posix_time) > int(most_recent_datapoint.posix_time):
                    self.array24hr.append(dpobject)
        else:
            self.array24hr = rawdata
        print("24 hr running array for " + self.name + " is " + str(len(self.array24hr)) + " records long.")

    def parse_dates(self, dpdata, dateregex):
        """Check for malformed datestrings and reject them"""
        pass

    def save_logfile(self):
        """Save the current data to CSV logfile"""
        RawlogName = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        RawlogName = self.logfile_dir + "/" + RawlogName + '.csv'
        try:
            with open(RawlogName, "w") as w:
                for data_point in self.array24hr:
                    w.write(data_point.print_values_utc() + "\n")
        except PermissionError:
            logging.error("ERROR: Permission error - unable to write logfile for " + str(self.name))

    def process_data(self):
        """Wrapper function to process this instruments data gathering and parameter updating
            get_raw_data() should return a "NULL" if the get was unsuccessful
        """
        raw_data = self.get_raw_data()

        if raw_data != "NULL":
            raw_data = self.parse_raw_data(raw_data)
            datapoint_list = self.convert_data(raw_data, self.dt_regex)
            self.append_raw_data(datapoint_list)
            self.array24hr = self.array24hr_prune(self.array24hr)
            self.array24hr_save()
            self.save_logfile()
        else:
            logging.error("ERROR: unable to GET data for " + str(self.name))
            print("ERROR: unable to GET data for " + str(self.name))


class MagnetometerWebCSV(Instrument):
            """Child class of Instrument - data from URL with CSV"""
            def __init__(self, name, location, owner, dt_regex, dt_format, datasource):
                Instrument.__init__(self, name, location, owner, dt_regex, dt_format, datasource)

            def get_raw_data(self):
                try:
                    response = requests.get(self.datasource)
                    webdata = response.content.decode('utf-8')
                    webdata = webdata.split("\n")
                except:
                    logging.error("ERROR: unable to get web data for " + self.name)
                    webdata = "NULL"
                return webdata

            def parse_raw_data(self, webdata):
                returndata = []
                for line in webdata:
                    # print(line)
                    logdata = line.strip()
                    logdata = logdata.split(",")
                    if (len(logdata) > 1):
                        # print(str(logdata) + " " + str(linecount))
                        dp_datetime = logdata[0]
                        dp_data = logdata[1]
                        dp = dp_datetime + "," + dp_data
                        returndata.append(dp)
                return returndata


class MagnetometerWebGOES(Instrument):
    """Child class of Instrument - data from the GOES satellites"""
    def __init__(self, name, location, owner, dt_regex, dt_format, datasource):
        Instrument.__init__(self, name, location, owner, dt_regex, dt_format, datasource)

    def get_raw_data(self):
        try:
            response = requests.get(self.datasource)
            webdata = response.content.decode('utf-8')
            webdata = webdata.split("\n")
        except:
            logging.error("ERROR: unable to get web data for " + self.name)
            webdata = "NULL"
        return webdata

    def parse_raw_data(self, webdata):
        returndata = []
        linecount = 0
        for line in webdata:
            linecount = linecount + 1
            line.strip()
            if linecount > 21:
                logdata = line.split()
                if len(logdata) > 0:
                    dp_date = logdata[0] + "-" + logdata[1] + "-" + logdata[2]
                    dp_time = logdata[3][:2] + ":" + logdata[3][2:]

                    dp_data = logdata[9]
                    dp_data = dp_data.split("e")
                    dp_data = dp_data[0]

                    dp = dp_date + " " + dp_time + "," + dp_data
                    returndata.append(dp)
        return returndata


class Discovr_Density_JSON(Instrument):
    """Child class of Instrument for the DISCOVR satellite solar wind data in JSON format"""
    def __init__(self, name, location, owner, dt_regex, dt_format, datasource):
        Instrument.__init__(self, name, location, owner, dt_regex, dt_format, datasource)

    def get_raw_data(self):
        webdata = "NULL"
        try:
            response = requests.get(self.datasource)
            webdata = response.json()
        except:
            logging.error("ERROR: error getting data from " + str(self.name))
        return webdata

    def parse_raw_data(self, rawdata):
        returndata = []
        try:
            json_data = rawdata
            for tple in json_data:
                time_tag = tple[0]
                density = tple[1]
                dp = time_tag + "," + density
                returndata.append(dp)
        except ValueError:
            logging.error("ERROR: no valid JSON data for " + str(self.name))
            print("ERROR: no valid JSON data for " + str(self.name))
        return returndata


# class MagnetometerDefault(Instrument):
#     def __init__(self, name, location, owner, dt_regex, dt_format, datasource):
#         Instrument.__init__(self, name, location, owner, dt_regex, dt_format, datasource)
#
#     def get_raw_data(self):
#         # try/except on get issue. Return a NULL if except
#         pass
#
#     def parse_raw_data(self):
#         # try/except on parsing issue.
#         returndata = []
#         return returndata
