# import mgr_database
import standard_stuff
# import plotter_spectrum_detailed
# import plotter_spectrum_quick
# import plotter_dual
# import plotter_current_day
# import plotter_fft_movie
# import plotter_phaseportrait
import time
from datetime import datetime, timezone
import os
import constants as k
import numpy as np


# This plotter will load data from CSV logfiles. This is an experiment to see if performance and speed are practically affected
#  and if this bypasses the weird SQLite file-access errors I've been having.
if __name__ == "__main__":
    # Decide on time interval we are plotting for. We can split off smaller intervals based on a larger list
    # Parse logfile directory for file names that fit our interval
    durate_seconds = 86400 * 7
    end_time = int(time.time())
    endfile = standard_stuff.posix2utc(end_time, '%Y-%m-%d') + '.csv'
    start_time = int(end_time - durate_seconds)
    startfile = standard_stuff.posix2utc(start_time, '%Y-%m-%d') + '.csv'

    logfile_list = os.listdir(k.dir_saves['logs'])
    logfile_list.sort()
    # Item is the filename. We can just use comparisons to identify files that are alphabetically in range
    # Those that are will have their data appended to a master list.
    for item in logfile_list:
        if item >= startfile:
            # "item <=" will include the current UTC day's data.
            if item <= endfile:
                print(item)


    # data = mgr_database.db_data_get(start_time, end_time)
    # data = mgr_database.db_data_all()
    print(f"*** Data downloaded from DB.")

    # # Basic cleanup of data.
    # # Matplotlib needs UTC time objects.
    # # Remove None from data and remove corresponding time objects from UTC time.
    # # We will allow the plotters to deal with gaps in data.
    # data_tilt = []
    # data_utc_objects = []
    # for psx, tilt in data:
    #     if isinstance(tilt, float):
    #         data_tilt.append(tilt)
    #         tim = datetime.fromtimestamp(psx, tz=timezone.utc)  # datetime object
    #         data_utc_objects.append(tim)
    #
    # # Send data to the plotters
    # plotter_dual.wrapper(data_utc_objects, data_tilt)
    # plotter_current_day.wrapper(data_utc_objects, data_tilt)
    # plotter_spectrum_detailed.wrapper(data_utc_objects, data_tilt)
    # plotter_spectrum_quick.wrapper(data_utc_objects, data_tilt)
    # plotter_fft_movie.wrapper(data_utc_objects, data_tilt)
    # # plotter_phaseportrait.wrapper(data_utc_objects, data_tilt)
    #
    # # Some stats on processing time.
    # elapsed_end = time.time()
    # elapsed_time = elapsed_end - elapsed_start
    # print(f"\n")
    # print(f"Readings per second: {len(data) / seconds_per_day}")
    # print(f"Elapsed time: {elapsed_time / 60:.2f} minutes")
    # print(f"*** All plots completed.")
