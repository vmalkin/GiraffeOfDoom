import os
import time
import constants as k
import mgr_database
import standard_stuff

def csv_save(parseddata):
    pass


    # Save data from the previous 48 to 24 hours. We will be backing up yesterday's data to CSV file. THis saves
    # the nuisance of accounting for dual dates and serves the purpose of a backup well enough.

    # for each item in parseddata
    # if file_name does not match item_date
    # create new file.
    # append item to file

