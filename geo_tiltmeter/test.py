from concurrent.futures import ProcessPoolExecutor
import class_aggregator
import standard_stuff
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.signal import butter, sosfiltfilt
import time
import os
import constants as k
import numpy as np
import multiprc_dual

if __name__ == '__main__':
    # each entry in data is [posix, data1, data2, etc].
    # The size of the FFT data we want to process (6 hours)
    print(f'*** BEGIN load CSV data ***')
    # Decide on time interval we are plotting for. We can split off smaller intervals based on a larger list
    # Parse logfile directory for file names that fit our interval
    # The Master List is no more than the last 7 days of data.
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
                        line = line.split(',')
                        l = [float(line[0]), float(line[1]), float(line[2]), float(line[3])]
                        masterlist.append(l)

    # We now have a master list of all data! Sort into order by posix time.
    masterlist.sort(key=lambda item: item[0])
    print(f'*** END load CSV data ***\n')

    # We do need to sanitise the master list. Nans must be deleted from seismic data
    sanitised_list = []
    for item in masterlist:
        if np.isnan(item[1]):
            print(f'{item} is purged.')
        else:
            sanitised_list.append(item)
    # CREATE aggregated data
    # [utc_object_time, seismic_data, temperature_data, pressure_data]
    print(f'*** BEGIN Plotter ***\n')
    one_day_slice_interval = -1 * (86400 * k.datapersecond) * 1
    one_day_slice = sanitised_list[one_day_slice_interval:]
    start = time.time()

    # window of 10 minutes
    window = 10 * 60 * k.datapersecond
    spectrumdata = class_aggregator.aggregate_data(window, one_day_slice)

    utc_object_time = spectrumdata[0]
    seismic_data = spectrumdata[1]
    temperature_data = spectrumdata[2]
    pressure_data = spectrumdata[3]
    rms_data = spectrumdata[4]
    stddev_data = spectrumdata[5]
    mean_data = spectrumdata[6]
    median_data = spectrumdata[7]
    skews_data = spectrumdata[8]
    kurts_data = spectrumdata[9]
    spectral_entropy_data = spectrumdata[10]

    print(len(spectral_entropy_data))
    # =========================================================
    # Some stats on processing time.
    end = time.time()
    elapsed_time = end - start
    print(f"\n")
    print(f"Elapsed time: {elapsed_time / 60:.2f} minutes.")
    print(f'\n*** END Plotter ***')