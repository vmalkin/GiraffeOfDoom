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
    # parse thru each file, extract date and data value
    #
    else:
        print("FILES.TXT does not exists. Create list of log files then rerun this script.")
