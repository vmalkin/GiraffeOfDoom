import standard_stuff as k
from os import path

# Index positions of UTC date and data in each logfile. This could be different...
index_utcdate = 0
index_data = 1

if __name__ == '__main__':
    # does files.txt exist? if not, abort
    if path.exists(k.file_list):
        pass
        # open each file in the list
        # parse thru each file, extract date and data value. If valid assemble into master list
        # Create a series of 365 dated bins for the previous 365 days
        # Remove any spikes in data with a median filter.
        # smooth the data
        # parse thru the list and allocate data values to bins (each bin will have a list of data for the day)
        # open the sightings file. allocate the dates to each bin.

    else:
        print("FILES.TXT does not exists. Create list of log files then rerun this script.")
