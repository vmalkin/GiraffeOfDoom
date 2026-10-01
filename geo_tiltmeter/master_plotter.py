# import mgr_database
import standard_stuff
# import plotter_spectrum_detailed
import plotter_spectrum_quick
import plotter_dual
import plotter_current_day
# import plotter_fft_movie
# import plotter_phaseportrait
import time
import class_aggregator
from datetime import datetime, timezone
import os
import constants as k
# import numpy as np

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
            # "item <= endfile" will include the current UTC day's data.
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

    # The next step is to decide what gets plotted as raw data, what gets turned into aggregated data for plotting, etc.
    # The aggregator effectively smooths data, so this does not need to happen in a plotter.
    # Matplotlib needs UTC time objects.

    # *** FFT DATA PROCESSING ***
    # fft_data is [utc_object_time_array, seismic_data_array]
    slice_interval = -86400 * k.sensor_reading_frequency
    raw_fft = masterlist[slice_interval:]
    fft_data = class_aggregator.aggregate_data(1, raw_fft)

    # plotter_spectrum_quick.wrapper(fft_data[0],fft_data[1])
    plotter_dual.wrapper(fft_data[0],fft_data[1])
    # plotter_current_day.wrapper(fft_data[0],fft_data[1])

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
