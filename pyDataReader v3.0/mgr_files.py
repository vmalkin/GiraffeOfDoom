import os
import logging
import datetime
errorloglevel = logging.ERROR
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)


class FileManager:
    def __init__(self):
        self.path_logs = "logs"
        self.path_charting = "highcharts"

        self.setup_paths()

    def setup_paths(self):
        # setup file paths
        # Set up file structure for Data logs. Linux systems might need use of the mode arg to set correct permissions.
        try:
            os.makedirs(self.path_logs)
            print("Logfile directory created.")
        except:
            if not os.path.isdir(self.path_logs):
                print("Unable to create log directory")
                logging.critical("CRITICAL ERROR: Unable to create logs directory")

        try:
            os.makedirs(self.path_charting)
            print("Graphing file directory created.")
        except:
            if not os.path.isdir(self.path_charting):
                print("Unable to create Graphing file directory")
                logging.critical("CRITICAL ERROR: Unable to create Graphing file directory")

    def save_daily_log(self, datapoint):
        # RAW log file name is created now. Get the date part of dt, add file suffix
        RawlogName = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        RawlogName = self.path_logs + "/" + RawlogName + '.csv'

        # If the logfile exists append the datapoint
        if os.path.isfile(RawlogName):
            try:
                with open(RawlogName, 'a') as f:
                    f.write(datapoint.print_values("posix") + '\n')
                    # print("Data logged ok. Array Size: " + str(len(readings)))
            except IOError:
                print("WARNING: There was a problem accessing the current logfile: " + RawlogName)
                logging.warning("WARNING: File IO Exception raised whilst accessing file: " + RawlogName)

        # ELSE add the header to the file because it is new
        else:
            try:
                with open(RawlogName, 'a') as f:
                    f.write(datapoint.print_labels() + '\n')

                print("Creating new logfile")
            except IOError:
                print("WARNING: There was a problem accessing the current logfile: " + RawlogName)
                logging.warning("WARNING: File IO Exception raised whilst accessing file: " + RawlogName)

    # #################################################################################
    # save an array to file
    # #################################################################################
    def savevalues(self, filename, array_name):
        # export array to array-save file
        try:
            with open(filename, 'w') as w:
                for dataObjects in array_name:
                    w.write(dataObjects + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + filename)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + filename)