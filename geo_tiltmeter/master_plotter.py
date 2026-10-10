from fontTools.ttLib.tables.S__i_l_f import Pass

import standard_stuff
import plotter_spectrum_quick
import plotter_dual
import plotter_current_day
import plotter_fft_movie
import time
import class_aggregator
import os
import constants as k
import numpy as np
from scipy.signal import butter, sosfiltfilt

# This plotter will load data from CSV logfiles. This is an experiment to see if performance and speed are practically affected
# and if this bypasses the weird SQLite file-access errors I've been having.

# We might be able to use a Pipe from the data writer to communicate it's current state, to know when it is safe to parse
# data files without causing a conflict
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

    # The next step is to decide what gets plotted as raw data, what gets turned into aggregated data for plotting, etc.
    # The aggregator effectively smooths data, so this does not need to happen in a plotter. Gaps in data might cause
    # spikes, so a median filter might be needed
    # Matplotlib needs UTC time objects.

    # CREATE aggregated data
    # [utc_object_time, seismic_data, temperature_data, pressure_data]
    print(f'*** BEGIN Plotter ***\n')
    slice_interval = -1 * 86400 * k.datapersecond
    slice_data = sanitised_list[slice_interval:]

    # =========================================================
    # Create Spectrogram and FFT Plots
    spectrumdata = class_aggregator.aggregate_data(1, slice_data)
    utctimes = spectrumdata[0]
    data = spectrumdata[1]
    # plotter_spectrum_quick.wrapper(utctimes, data)
    # plotter_fft_movie.wrapper(utctimes, data)

    # # =========================================================
    # # Seven Day Plotter
    # window = k.datapersecond * 60
    # seven_day_data = class_aggregator.aggregate_data(window, sanitised_list)
    # # Get tilt, temperature and pressure data.
    # utctimes = seven_day_data[0]
    # data = seven_day_data[1]
    # print(f'{len(utctimes)} {len(slice_data[1])}')
    # temperature = seven_day_data[2]
    # pressure = seven_day_data[3]
    # # Smooth the data
    # smoothinghalfwindow = k.datapersecond * 1
    # data = standard_stuff.filter_average(data, smoothinghalfwindow)
    # temperature = standard_stuff.filter_average(temperature, smoothinghalfwindow)
    # pressure = standard_stuff.filter_average(pressure, smoothinghalfwindow)
    # utctimes = utctimes[smoothinghalfwindow:-smoothinghalfwindow]
    # #
    # print(f'{len(utctimes)} {len(data)} {len(temperature)} {len(pressure)} \n')
    # plotter_current_day.wrapper(
    #     utctimes=utctimes,
    #     data=data,
    #     temperature=temperature,
    #     pressure=pressure,
    #     title='Seven Day Plot',
    #     filename='seven_day.png'
    # )

    # =========================================================
    # Dual plotter.
    # We will recycle the existing spectrumdata.
    utctimes = spectrumdata[0]
    data = spectrumdata[1]
    #
    # de-mean the data.
    data = data - np.mean(data)
    #
    # Apply a butterworth filter to isolate seismic signal. To avoid shifting the data in time (phase) we will use
    # sosfiltfilt.
    sos = butter(
        4,
        [0.01, 0.1],
        btype='bandpass',
        fs=k.datapersecond,
        output='sos'
    )
    data_filtered = sosfiltfilt(sos, data)
    #
    data_dx = []
    for i in range(1, len(data)):
        dx = data_filtered[i] - data_filtered[i - 1]
        data_dx.append(dx)
    # dx-ing the data loses a value, so prune data nd time arrays to be the same length otherwise we will have errors
    # when trying to plot things.
    utctimes = utctimes[1:]
    data_filtered = data_filtered[1:]
    #
    # Smooth the data_dx
    print('smoothing dx...')
    halfwindow = k.datapersecond * 1
    data_dx = standard_stuff.filter_average(data_dx, halfwindow)
    utctimes = utctimes[halfwindow:-1 * halfwindow]
    data_filtered = data_filtered[halfwindow:-1 * halfwindow]
    #
    data_dx = standard_stuff.filter_average(data_dx, halfwindow)
    utctimes = utctimes[halfwindow:-1 * halfwindow]
    data_filtered = data_filtered[halfwindow:-1 * halfwindow]
    plotter_dual.wrapper(utctimes, data_filtered, data_dx)

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
