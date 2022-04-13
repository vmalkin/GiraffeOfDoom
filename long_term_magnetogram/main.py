import standard_stuff as k
from os import path
import re

# Index positions of UTC date and data in each logfile. This could be different...
index_utcdate = 0
index_data = 1
regex = "\d\d\d\d-\d\d-\d\d.csv"

# Create a bin object. A bin:
# Covers a time period
# Has a list of data values for the time period
# Identifies if there was a magnetic storm for the time period
# Identifies if there were sightings recorded for the time period
# Can output time and data values as CSV formatted string.
# Can return a CSV formatted header for data

if __name__ == '__main__':
    masterlist = []
    # does files.txt exist? if not, abort
    if path.exists(k.file_list):
        # load files.txt
        with open(k.file_list, "r") as f:
            for line in f:
                if re.match(regex, line):
                    # open each file in the list
                    # parse thru each file, extract date and data value. If valid assemble into master list
                    with open(line, "r") as csvdata:
                        for csvline in csvdata:
                            csvline = csvline.strip()
                            csvline = csvline.split(",")
                            posixtime = k.utc2posix(csvline[0], '%Y-%m-%d %H:%M:%S')
                            data = csvline[index_data]
                            dp = [posixtime, data]
                            masterlist.append(dp)
        # Sort by date
        masterlist.sort()

        # Create a series of 365 dated bins for the previous 365 days
        # Remove any spikes in data with a median filter.
        # smooth the data
        # parse thru the list and allocate data values to bins (each bin will have a list of data for the day)
        # open the sightings file. allocate the dates of sightings to each bin.

    else:
        print("FILES.TXT does not exists. Create list of log files then rerun this script.")
