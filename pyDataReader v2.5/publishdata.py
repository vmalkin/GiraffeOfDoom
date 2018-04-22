#!usr/bin/python
import DataProcessor_library as dp
import mgr_files as ofm
import time
import constants as k
import random
import logging
import mgr_binner as binner
import mgr_dhdt as df
# from constants import mag_readings

# #################################################################################
# Publisher script
# As processing data can take considerable time (up to several seconds) running this
# in sequence with the datalogging may cause bottlenecks, esp when working as a rapid-run
# magnetometer. The simplest solution is to run the processor in parallel with the
# logging script. Managing concurrent python scripts is easily done thru
# appropriate batch/bash scripting
# #################################################################################
RANDOM_SECS = 10                # To randomise the minutes delay
DELAY_SHORT_INTERVAL = 240       # THE DELAY INTERVAL FOR FILE COPYING

# Setup error/bug logging
logging.basicConfig(filename="publisherrors.log", format='%(asctime)s %(message)s')

# #################################################################################
# FUNCTION DEFINITIONS
# Calculate the differences
# #################################################################################
def process_data(input_data_array):
    # If necessary, invert the data so that trends up mean increasing field strength
    data_array = dp.invert_data_array(input_data_array)

    # create the array of dF/dt
    diffs_data = df.create_diffs_array(data_array)

    # recalculate and save a corrected display file free from blips
    # rebuild = False
    rebuild = False
    if rebuild == True:
        rebuilt_data = df.rebuild_originaldata(diffs_data)
    else:
        rebuilt_data = data_array

    # smooth the diffs to show the trend. Two passes at 5 minutes is usually ok.
    window = k.MAG_READ_FREQ * 5
    diffs_data = df.running_average(diffs_data, window)
    diffs_data = df.running_average(diffs_data, window)

    # calculate the minimum rate of change from THIS smoothed data. append this range to the data. Highcharts
    # will display this as +/- ve bars on the chart
    diffs_data = df.calculate_minmax_values(diffs_data)

    # add the CSV file headers
    headerstring = "Date/time UTC, Min for hour, Max for hour, dH/dt"
    diffs_data.reverse()
    diffs_data.append(headerstring)
    diffs_data.reverse()

    # Save out the diffs array
    df.savevalues(k.FILE_4DIFFS, diffs_data)


    # # SMooth the data slightly
    # smoothed_data_array = dp.running_average(rebuilt_data, 6)
    #
    # to get the last 1 hours the split value is mag read frequency * 60 * 1
    splitvalue = k.MAG_READ_FREQ * 60 * 1
    ofm.create_hichart_datafile(rebuilt_data, splitvalue, k.FILE_1HR)
    #
    
    # to get the last 1 MINUTE the split value is mag read frequency * 1
    ofm.create_hichart_datafile_brendan(rebuilt_data, 60, "brendan.csv")

    
    #
    # to get the last 24 hours the split value is mag read frequency * 60 * 24
    splitvalue = k.MAG_READ_FREQ * 60 * 24
    ofm.create_hichart_datafile(rebuilt_data, splitvalue, k.FILE_24HR)

    # Create the 1 minute bin file
    binned_data = binner.utc2unix(data_array)
    binned_data = binner.binsimple(binned_data)
    binned_data = binner.unix2utc(binned_data)
    binner.SaveRawArray(binned_data)

# #################################################################################
# Main program starts here. Set appropriate delay for tapping into the main arraysave
# file to minimise r/w conflicts
# #################################################################################
while True:
    # how long to perform all the operations
    starttime = time.time()
    mag_readings = []

# try:
    mag_readings = ofm.CreateRawArray()
    process_data(mag_readings)

# except:
    print("ERROR: Problem opening file")
    logging.critical(" ERROR: Problem opening file. Unable to create display files")

    # Calculate the processing time
    endtime = time.time()
    processingtime = endtime - starttime
    processingtime = str(processingtime)[:5]
    print("Processing complete. Elapsed time: " + processingtime + " seconds.\n")

    timedelay = DELAY_SHORT_INTERVAL + random.randint(0,RANDOM_SECS)
    time.sleep(timedelay)
