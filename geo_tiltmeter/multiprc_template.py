# This template uses multiprocessing to iterate over very large arrays of data. We will use the
# ProcessPoolExecutor as it's considered the more modern method.
# Yes - AI has helped me with the ideas, but as you can tell by the janky code, that bit is mine.
from concurrent.futures import ProcessPoolExecutor
import standard_stuff
import time
import os
import constants as k
import numpy as np


# There may be other functions here called by process_chunk


def process_chunk(chunk):
    # This is a _Worker_ which typically uses the chunk to process then generate a
    # single plot from this chunk. Return the filename of the plot.
    return filename


def chunks(data, size):
    # In Python, yield turns a normal function into a generator so
    # it can produce values one at a time instead of returning everything at once.
    # Each time the generator runs up to a yield, it pauses and gives the value to
    # the caller, then continues later from where it left off. THis memory efficient
    for i in range(0, len(data), size):
        yield data[i:i + size]


def main():
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
    two_day_slice_interval = -1 * (86400 * k.datapersecond) * 2
    two_day_slice = sanitised_list[two_day_slice_interval:]
    chunksize = 10000
    cores = 3
    with ProcessPoolExecutor(max_workers=cores) as executor:
        results = list(
            executor.map(
                process_chunk,
                chunks(two_day_slice, chunksize)
        )
    )
    return results

if __name__ == '__main__':
    main()