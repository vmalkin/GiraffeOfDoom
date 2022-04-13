import standard_stuff as k
from os import path
import re

# Index positions of UTC date and data in each logfile. This could be different...
index_utcdate = 0
index_data = 1
regex_filename = "\d\d\d\d-\d\d-\d\d.csv"

# Create a bin object. A bin:
# Covers a time period
# Has a list of data values for the time period
# Identifies if there was a magnetic storm for the time period
# Identifies if there were sightings recorded for the time period
# Can output time and data values as CSV formatted string.
# Can return a CSV formatted header for data
class Bin:
    def __init__(self, time):
        self.time = time
        self.data = []
        self.sighting = 0

    def avg_dhdt(self):
        pass

    def return_reportstring(self):
        pass


if __name__ == '__main__':
    regex_data = "[0-9][.][0-9]"
    masterlist = []

    # does files.txt exist? if not, abort
    if path.exists(k.file_list):
        # load files.txt
        with open(k.file_list, "r") as filelist:
            for filename in filelist:
                nw_filename = filename.strip()
                if re.match(regex_filename, nw_filename):
                    # open each file in the list
                    # parse thru each file, extract date and data value. If valid assemble into master list
                    with open(nw_filename, "r") as csvdata:
                        for csvline in csvdata:
                            newcsv = csvline.strip()
                            newcsv = newcsv.split(",")
                            # If we have data and not a header
                            if re.match(regex_data, newcsv[index_data]):
                                posixtime = k.utc2posix(newcsv[0], '%Y-%m-%d %H:%M:%S')
                                data = newcsv[index_data]
                                dp = [posixtime, data]
                                masterlist.append(dp)
        # Sort by date
        masterlist.sort()


        # Remove any spikes in data with a median filter.
        # smooth the data
        # Create a series of 365 dated bins for the previous 365 days
        # parse thru the list and allocate data values to bins (each bin will have a list of data for the day)
        # open the sightings file. allocate the dates of sightings to each bin.

    else:
        print("FILES.TXT does not exists. Create list of log files then rerun this script.")
