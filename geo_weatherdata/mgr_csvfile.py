import os
import time
import constants as k
import mgr_database
import standard_stuff

def csv_save():
    # Save data from the previous 48 to 24 hours. We will be backing up yesterday's data to CSV file. THis saves
    # the nuisance of accounting for dual dates and serves the purpose of a backup well enough.
    t = time.time()
    utc_end_time = standard_stuff.posix2utc(t, timeformat='%Y-%m-%d')
    psx_end_time = standard_stuff.utc2posix(utc_end_time, timeformat='%Y-%m-%d')
    psx_start_time = psx_end_time - 86400

    current_csv_backup = f"{k.dir_saves['logs']}/{utc_end_time}.csv"

    if not os.path.exists(current_csv_backup):
        data = mgr_database.db_data_get(psx_start_time, psx_end_time)
        with open(current_csv_backup, 'w', newline='') as c:
            for psx, temp, prs in data:
                # print(f"{psx},{temp},{prs}\n")
                c.write(f"{psx},{temp},{prs}\n")
        c.close()

