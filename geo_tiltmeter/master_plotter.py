import standard_stuff
import plotter_spectrum_quick
import multiprc_dual
import plotter_current_day
import multiprc_fft
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
    one_day_slice_interval = -1 * (86400 * k.datapersecond) * 1
    one_day_slice = sanitised_list[one_day_slice_interval:]

    # =========================================================
    # Create Spectrogram
    print(f'*** Spectrograms')
    spectrumdata = class_aggregator.basic_aggregated_list(one_day_slice,0)
    utctimes = []
    data = []
    for item in spectrumdata:
        dd = item.get_data_avg(item.data_seismo)
        to = item.return_utc_timeobject(item.get_avg_posix())
        data.append(dd)
        utctimes.append(to)
    frq = 10
    plotter_spectrum_quick.wrapper(
        utc=utctimes,
        data=data,
        fs=frq,
        nfft=8192,
        fmin=10 ** -3,
        fmax=5 * 10 ** 0,
        title="Quick spectrum",
        savefile="spec_quick.png"
    )

    # =========================================================
    # One Day Plotter
    print(f'*** One-day plot.')
    hlfwindow = k.datapersecond * 30
    spectrumdata = class_aggregator.basic_aggregated_list(one_day_slice,hlfwindow)
    utctimes = []
    data = []
    temperature = []
    pressure = []
    for item in spectrumdata:
        dd = item.get_data_avg(item.data_seismo)
        tt = item.get_data_avg(item.data_temperature)
        pp = item.get_data_avg(item.data_pressure)
        to = item.return_utc_timeobject(item.get_avg_posix())
        data.append(dd)
        temperature.append(tt)
        pressure.append(pp)
        utctimes.append(to)

    deltapressure = []
    for i in range(1, len(pressure)):
        d = pressure[i] - pressure[i - 1]
        deltapressure.append(d)
    deltapressure.append(d)

    plotter_current_day.wrapper(
        utctimes=utctimes,
        data=data,
        temperature=temperature,
        pressure=pressure,
        deltapressure=deltapressure,
        title='One Day Plot',
        filename='one_day.png'
    )

    # =========================================================
    # Seven Day Plotter
    print(f'*** Seven-day plot.')
    hlfwindow = 5 * 60 * k.datapersecond
    spectrumdata = class_aggregator.basic_aggregated_list(sanitised_list, hlfwindow)
    utctimes = []
    data = []
    temperature = []
    pressure = []
    for item in spectrumdata:
        dd = item.get_data_avg(item.data_seismo)
        tt = item.get_data_avg(item.data_temperature)
        pp = item.get_data_avg(item.data_pressure)
        to = item.return_utc_timeobject(item.get_avg_posix())
        data.append(dd)
        temperature.append(tt)
        pressure.append(pp)
        utctimes.append(to)

    deltapressure = []
    for i in range(1, len(pressure)):
        d = pressure[i] - pressure[i - 1]
        deltapressure.append(d)
    deltapressure.append(d)

    # # Smooth the data
    # smoothinghalfwindow = 2
    # data = standard_stuff.filter_average(data, smoothinghalfwindow)
    # temperature = standard_stuff.filter_average(temperature, smoothinghalfwindow)
    # pressure = standard_stuff.filter_average(pressure, smoothinghalfwindow)
    # deltapressure = standard_stuff.filter_average(deltapressure, smoothinghalfwindow)
    # utctimes = utctimes[smoothinghalfwindow:-smoothinghalfwindow]
    # #
    # print(f'{len(utctimes)} {len(data)} {len(temperature)} {len(pressure)} \n')
    plotter_current_day.wrapper(
        utctimes=utctimes,
        data=data,
        temperature=temperature,
        pressure=pressure,
        deltapressure=deltapressure,
        title='Seven Day Plot',
        filename='seven_day.png'
    )
    #
    # # =========================================================
    # # Basic seismic curve.
    # one_day_data = class_aggregator.aggregate_data(0,1, one_day_slice, mode='basic')
    # utctimes = one_day_data[0][2]
    # data = one_day_data[1][2]
    # # use a 4-pole butterworth filter to get the seismic signals
    # sos = butter(
    #     4,
    #     [0.0001, 0.3],
    #     btype='bandpass',
    #     fs=k.datapersecond,
    #     output='sos'
    # )
    # filtered = sosfiltfilt(sos, data)
    # multiprc_dual.main(utctimes, filtered)

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
