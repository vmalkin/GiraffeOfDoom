#!usr/bin/python
import dataprocessor_library as dp
import filemanager_library as ofm
import time

# #################################################################################
# Publisher script
# As processing data can take considerable time (up to several seconds) running this
# in sequence with the datalogging may cause bottlenecks, esp when working as a rapid-run
# magnetometer. The simplest solution is to run the processor in parallel with the
# logging script. Managing concurrent python scripts is easily done thru
# appropriate batch/bash scripting
# #################################################################################


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
    data_array = dp.datafilters_library.median_filter_3values(data_array) # Median filter to remove blips
    smoothed_data_array = dp.running_average(data_array) # smooth the array

    # ###########################################################################
    # CReate the differences array and smooth.
    # Do Not Use the smoothed data from previous step. Use original data
    # do several iterations to ensure best appearance.
    # This differences data is used to display rates of change, and minimises the effect
    # of diurnal variation, allowing us to see rapid onsets/changes in the magnetic field.
    # ###########################################################################
    output_diffs = dp.create_diffs_array(data_array)
    for i in range(0,2):
        output_diffs = dp.diffs_running_average(output_diffs)

    # ###########################################################
    # create the display files for graphing, using ArraySave.CSV
    #
    # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    #
    # ###########################################################
    ofm.Create24(smoothed_data_array)
    ofm.Create4(smoothed_data_array)
    ofm.CreateDiffs(output_diffs) # use output_diffs data
    dp.binnedaverages(data_array) # use original data

    # # ########################################################
    # # create the display files for graphing, using Diffs.csv
    # # use this if we are having major problems with spikes
    # # in final display files
    # # ########################################################
    # smoothed_data_array = dp.readings_from_diffs(output_diffs)
    # ofm.Create24(smoothed_data_array)
    # ofm.Create4(smoothed_data_array)
    # ofm.CreateDiffs(output_diffs) # use output_diffs data
    # datafilters.binnedaverages(smoothed_data_array) # use original data


# #################################################################################
# Main program starts here. Set appropriate delay for tapping into the main arraysave
# file to minimise r/w conflicts
# #################################################################################
while True:
    # we might want to have some means of publishing different files at different rates
    readings = []

    dp.CreateRawArray(readings)

    process_data(readings)

    time.sleep(300)
