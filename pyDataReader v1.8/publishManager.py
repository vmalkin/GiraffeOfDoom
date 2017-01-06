#!usr/bin/python
import DataProcessor_library as dp
import datafilters_library
import OutputFileManager_library as ofm
import time


# #################################################################################
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
    smoothed_data_array = datafilters_library.running_average(data_array) # smooth the array

    # ###########################################################################
    # CReate the differences array and smooth.
    # Do Not Use the smoothed data from previous step. Use original data
    # do several iterations to ensure best appearance.
    # This differences data is used to display rates of change, and minimises the effect
    # of diurnal variation, allowing us to see rapid onsets/changes in the magnetic field.
    # ###########################################################################
    output_diffs = dp.create_diffs_array(data_array)
    for i in range(0,2):
        output_diffs = datafilters_library.diffs_running_average(output_diffs)

    # ###########################################################
    # create the display files for graphing, using ArraySave.CSV
    #
    # COMMENT OUT THESE LINES IF WE'RE USING THE DIFFS.CSV FILE TO CREATE OUR DISPLAY FILES
    #
    # ###########################################################
    ofm.Create24(smoothed_data_array)
    ofm.Create4(smoothed_data_array)
    ofm.CreateDiffs(output_diffs) # use output_diffs data
    datafilters_library.binnedaverages(data_array) # use original data

    # # ########################################################
    # # create the display files for graphing, using Diffs.csv
    # # use this if we are having major problems with spikes
    # # in final display files
    # # ########################################################
    # smoothed_data_array = ofm.readings_from_diffs(output_diffs)
    # ofm.Create24(smoothed_data_array)
    # ofm.Create4(smoothed_data_array)
    # ofm.CreateDiffs(output_diffs) # use output_diffs data
    # datafilters.binnedaverages(smoothed_data_array) # use original data


while True:
    readings = []

    dp.CreateRawArray(readings)

    process_data(readings)

    time.sleep(300)
