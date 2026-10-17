import standard_stuff
import time
import class_aggregator
import os
import constants as k
import numpy as np


# This plotter will load data from CSV logfiles. This is an experiment to see if performance and speed are practically affected
# and if this bypasses the weird SQLite file-access errors I've been having.

# We might be able to use a Pipe from the data writer to communicate it's current state, to know when it is safe to parse
# data files without causing a conflict
def plot(utcobjects, data, med, max, min, std):
    pass


if __name__ == "__main__":
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
    # two_day_slice_interval = -1 * (86400 * k.datapersecond) * 2
    one_day_slice = sanitised_list[one_day_slice_interval:]
    # two_day_slice = sanitised_list[two_day_slice_interval:]

    # format is
    #  [utc_object_time, seismic_data, temperature_data, pressure_data]
    bin_window = 1
    binned_data = class_aggregator.aggregate_data(bin_window, one_day_slice)

    half_window = k.datapersecond * 60 * 2.5
    utctimestamp = []
    median_reading = []
    mean_reading = []
    max_reading = []
    min_reading = []
    standard_dev = []
    temp_reading = []

    for i in range(0, len(binned_data)):
        temp_reading.append(binned_data[i][1])
        if len(temp_reading) >= ((2 * half_window) + 1):
            utctimestamp.append(binned_data[i - half_window][0])
            median_reading.append(np.median(temp_reading))
            mean_reading.append(np.mean(temp_reading))
            max_reading.append(np.max(temp_reading))
            min_reading.append(np.min(temp_reading))
            standard_dev.append(np.std(temp_reading))
            temp_reading.pop(0)

    plot(
        utcobjects=utctimestamp,
        data=median_reading,
        med=median_reading,
        max=max_reading,
        min=min_reading,
        std=standard_dev
    )

    # =========================================================
    # Some stats on processing time.
    data_end = masterlist[0][0]
    data_start = masterlist[-1][0]
    data_length = len(masterlist)
    readingspersecond = data_length / (data_start - data_end)
    elapsed_end = time.time()
    elapsed_time = elapsed_end - end_time
    print(f"\n")
    print(f'Sensor is running at {readingspersecond}  readings per second.')
    print(f"Elapsed time: {elapsed_time / 60:.2f} minutes.")
    print(f'\n*** END Plotter ***')
