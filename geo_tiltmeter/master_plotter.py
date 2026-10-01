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


class Aggregator:
    # This object allows us to aggregate data into whatever interval we choose.
    def __init__(self, posixstart, posixstop):
        self.data_null = np.nan
        self.date_start = posixstart  # should be POSIX values
        self.date_stop = posixstop  # should be POSIX values
        self.data_seismo = []
        # self.data_temperature = []
        # self.data_pressure = []

    def get_data_avg(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        val_avg = self.data_null
        if len(dataset) > 0:
            try:
                val_avg = round(np.nanmean(dataset), 4)
                return val_avg
            except:
                return val_avg

    def get_data_median(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        val_median = self.data_null
        if len(dataset) > 0:
            try:
                val_median = round(np.nanmedian(dataset), 4)
                return val_median
            except:
                return val_median

    def get_data_max(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        val_max = self.data_null
        if len(dataset) > 0:
            try:
                val_max = round(np.nanmax(dataset), 4)
                return val_max
            except:
                return val_max

    def get_data_min(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        if len(dataset) > 0:
            val_min = round(np.nanmin(dataset), 4)
        else:
            val_min = self.data_null
        return val_min

    def get_avg_posix(self):
        avg_time = round((self.date_start + self.date_stop) / 2, 4)
        return avg_time

    def return_utc_object(self, posixvalue):
        tim = datetime.fromtimestamp(posixvalue, tz=timezone.utc)  # datetime object
        return tim


# This plotter will load data from CSV logfiles. This is an experiment to see if performance and speed are practically affected
# and if this bypasses the weird SQLite file-access errors I've been having.

# We might be able to use a Pipe from the data writer to communicate it's current state, to know when it is safe to parse
# data files without causing a conflict
if __name__ == "__main__":
    # Current data format!
    # [posixtime, tiltdata]

    # Decide on time interval we are plotting for. We can split off smaller intervals based on a larger list
    # Parse logfile directory for file names that fit our interval
    duration_seconds = 86400 * 7
    end_time = int(time.time())
    endfile = standard_stuff.posix2utc(end_time, '%Y-%m-%d') + '.csv'
    start_time = int(end_time - duration_seconds)
    startfile = standard_stuff.posix2utc(start_time, '%Y-%m-%d') + '.csv'

    # Get the list of logfiles
    logfile_list = os.listdir(k.dir_saves['logs'])
    logfile_list.sort()

    # Item is the filename. We can just use comparisons to identify files that are alphabetically in range
    # Those that are will have their data appended to a master list.
    masterlist = []
    for item in logfile_list:
        if item >= startfile:
            # "item <=" will include the current UTC day's data.
            if item <= endfile:
                # to load the file, dont forget to prepend the path to the file!
                logfile = k.dir_saves['logs'] + os.sep + item
                with open(logfile, 'r') as f:
                    for line in f:
                        # remove the carriage return
                        line = line.strip()
                        masterlist.append(line)

    # We now have a master list of all data! Sort into order by posix time.
    masterlist.sort(key=lambda item: item[0])









    # data = mgr_database.db_data_get(start_time, end_time)
    # data = mgr_database.db_data_all()
    # print(f"*** Data downloaded from DB.")



    # Basic cleanup of data.
    # Matplotlib needs UTC time objects.
    # Remove None from data and remove corresponding time objects from UTC time.

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
