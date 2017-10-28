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

    # # SMooth the data slightly
    # smoothed_data_array = dp.running_average(data_array, 6)
    #
    # # to get the last 1 hours the split value is mag read frequency * 60 * 1
    # splitvalue = k.MAG_READ_FREQ * 60 * 1
    # ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_1HR)
    #
    # # to get the last 4 hours the split value is mag read frequency * 60 * 4
    # splitvalue = k.MAG_READ_FREQ * 60 * 4
    # ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_4HR)
    #
    # # to get the last 24 hours the split value is mag read frequency * 60 * 24
    # splitvalue = k.MAG_READ_FREQ * 60 * 24
    # ofm.create_hichart_datafile(smoothed_data_array, splitvalue, k.FILE_24HR)

    # create the differences array from the raw data
    df.process_differences(input_data_array)

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
    try:
        mag_readings = ofm.CreateRawArray()
        process_data(mag_readings)
    except:
        print("ERROR: Problem opening ArraySave file")
        logging.critical(" ERROR: Problem opening file. Unable to create display files")

    # Calculate the processing time
    endtime = time.time()
    processingtime = endtime - starttime
    processingtime = str(processingtime)[:5]
    print("Processing complete. Elapsed time: " + processingtime + " seconds.\n")

    timedelay = DELAY_SHORT_INTERVAL + random.randint(0,RANDOM_SECS)
    time.sleep(timedelay)
