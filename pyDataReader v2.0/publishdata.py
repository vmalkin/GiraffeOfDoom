#!usr/bin/python
import DataProcessor_library as dp
import filemanager_library as ofm
import time
import constants as k
import random
import logging
import binlibrary as binner
import difference_creator as df
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

    # ###########################################################################
    # Initial filter of data: smoothing, remove transients, etc
    # We're only doing a running average at the moment, but we could add anything,
    # median filter etc...
    # This smoothed data is used to create the magnetogram display files.
    #
    # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    #
    # ###################################### #####################################
    # data_array = dp.median_filter_3values(data_array)

    # ###########################################################################
    # CReate the differences array and smooth.
    # Do Not Use the smoothed data from previous step. Use original data
    # do several iterations to ensure best appearance.
    # This differences data is used to display rates of change, and minimises the effect
    # of diurnal variation, allowing us to see rapid onsets/changes in the magnetic field.
    # ###########################################################################

    # create the differences array from the raw data
    output_diffs = df.process_differences(input_data_array)

    # rebuild the relative readings, now with no blips
    SPIKE_CHECK = False
    smoothed_data_array = []

    if SPIKE_CHECK == True:
        print("Spike checking ON - rebuilding display data")
        smoothed_data_array = dp.readings_from_diffs(output_diffs)
    else:
        print("Spike checking OFF - using raw magnetometer data")
        smoothed_data_array = data_array

    # SMooth the data slightly
    smoothed_data_array = dp.running_average(smoothed_data_array, 6)

    # smoothed for two by 5 minutes here




    # ###########################################################
    # create the display files for graphing, using ArraySave.CSV
    #
    # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    #
    # ###########################################################

    ofm.CreateDiffs(output_diffs) # use output_diffs data
    # append the min/max background values. Changing the smoothing values WILL change this so be aware
    dp.find_avg_background()


    # to get the last 1 hours the split value is mag read frequency * 60 * 1
    splitvalue = k.MAG_READ_FREQ * 60 * 1
    ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_1HR)

    # to get the last 4 hours the split value is mag read frequency * 60 * 4
    splitvalue = k.MAG_READ_FREQ * 60 * 4
    ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_4HR)

    # to get the last 24 hours the split value is mag read frequency * 60 * 24
    splitvalue = k.MAG_READ_FREQ * 60 * 24
    ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_24HR)

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
    # Calculate the processing time
    endtime = time.time()
    processingtime = endtime - starttime
    processingtime = str(processingtime)[:5]
    print("Processing complete. Elapsed time: " + processingtime + " seconds.\n")
    # print(str(len(mag_readings)) + " records loaded")

    # except:
    #     print("ERROR: Problem opening file")
    #     logging.critical(" ERROR: Problem opening file. Unable to create display files")


    timedelay = DELAY_SHORT_INTERVAL + random.randint(0,RANDOM_SECS)
    time.sleep(timedelay)
